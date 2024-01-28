from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from rest_framework import status
from django.http import Http404
import re

from horarios.models import ComponenteCurricular, Professor, Turma
from .serializers import ComponenteCurricularSerializer, ProfessorSerializer, TurmaSerializer, \
    TurmaSerializerFormatado, HorariosSerializer, ConflitosSerializer


# View que está mostrando todos os objetos criados de Componente Curricular
class ComponenteCurricularViewSet(viewsets.ModelViewSet):
    queryset = ComponenteCurricular.objects.all()
    serializer_class = ComponenteCurricularSerializer
    permission_classes = [IsAuthenticated]

    # Função para validar o código de um componente curricular
    def validate_codigo_componente(self, codigo):
        # Verifica se o código não está vázio
        if len(codigo) < 1:
            return f"É necessário informar o código do componente."

        # Verifica se o código possui o tamanho correto
        if len(codigo) != 7:
            return f"O código do componente deve ter 7 caracteres alfanuméricos."

        # Verifica se o código está no formato correto com uso de regex (Ex. LLL0000)
        if not re.match(r'^([A-Z]{3})([0-9]{4})$', codigo):
            return f"Formato inválido do código ({codigo})."

        # Verifica se o código passado corresponde a um componente já existente
        try:
            componente = self.queryset.get(pk=codigo)
            if componente:
                return f"Já existe um componente com esse código ({codigo})."
        except ObjectDoesNotExist:
            pass

    # Função para validar o nome de um componente curricular
    def validate_nome_componente(self, nome):
        # Verifica se o campo nome do componente é uma String
        if not isinstance(nome, str):
            return f"O campo de nome do componente deve ser uma String."

        # Verifica se o nome do componente contém pelo menos um caractere
        if len(nome) < 1:
            return f'É necessário informar o nome do componente.'

        # Verifica se o nome do componente contém pelo menos um caractere
        if len(nome) > 80:
            return f'O nome do componente deve ter no máximo 80 caracteres.'

        # Verifica se o nome do componente contém apenas letras e espaços, nada de caracteres especiais
        padrao = re.compile(r'[a-zA-ZÀ-ú\s]+')
        if not padrao.fullmatch(nome):
            return f"O nome do componente deve conter apenas letras e espaços."

    # Função para validar o número do semestre de um componente curricular
    def validate_semestre_componente(self, semestre, obrigatorio):
        try:
            semestre = int(semestre)
        except ValueError:
            return f"O campo de número de semestre deve ser um número inteiro."

        # Verifica se o semestre é realmente um número inteiro
        # if not isinstance(semestre, int):
            # return f"O campo de número de semestre deve ser um número inteiro."

        # Verifica se o semestre é um número menor que 0
        if int(semestre) < 0:
            return f"O número do semestre ({semestre}) deve ser maior ou igual a 0."

        # Verifica se o semestre é um número maior que 6
        if int(semestre) > 6:
            return f"O número do semestre ({semestre}) deve ser menor ou igual a 6."

        # Verifica se o campo obrigatório é do tipo Boolean
        if not isinstance(obrigatorio, bool):
            return f"O campo obrigatório deve ter um valor booleano (True ou False)."

        # Verifica se o componente é obrigatório com semestre igual a 0
        if int(semestre) == 0 and obrigatorio:
            return f"O componente quando obrigatório deve possuir um semestre diferente de 0."

    # Função para validar a carga horária de um componente curricular
    def validate_carga_componente(self, carga):
        # Verifica se a carga horária do componente foi informada
        if not carga:
            return f'É necessário informar uma carga horária para o componente.'

        try:
            carga = int(carga)
        except ValueError:
            return f"O campo da carga horário deve ser um número inteiro."

        # Verifica se a carga horário do componente é realmente um número inteiro
        # if not isinstance(carga, int):
            # return f"O campo da carga horário deve ser um número inteiro."

        # Verifica se a carga horária do componente é divisível por 15 e maior que 0
        if int(carga) < 0 or not int(carga) % 15 == 0:
            return f'Carga horária ({carga}) deve maior que 0 e divisível por 15.'

    # Função para validar o departamento de um componente curricular
    def validate_departamento(self, departamento):
        # Verifica se o departamento do componente está dentro das possibilidades
        if departamento not in [dep[0] for dep in ComponenteCurricular.DEPARTAMENTO]:
            return f'É necessário informar um departamento válido.'

    # Função para validar um componente curricular
    def validate_componente(self, componente, request=""):
        validation_errors = {}

        # Verifica se o campo codigo está dentro do corpo da requisição, se sim, chama a sua função de validação
        if 'codigo' in componente:
            codigo = self.validate_codigo_componente(componente.get("codigo").upper())
            if codigo:
                validation_errors['codigo'] = codigo
        # Senão, informa que o campo é obrigatório caso a requisição não seja PATCH
        elif request != "PATCH":
            validation_errors['codigo'] = f'Campo obrigatório.'

        # Verifica se o campo nome_comp está dentro do corpo da requisição, se sim, chama a sua função de validação
        if 'nome_comp' in componente:
            nome_comp = self.validate_nome_componente(componente.get("nome_comp").upper())
            if nome_comp:
                validation_errors['nome_comp'] = nome_comp
        # Senão, informa que o campo é obrigatório caso a requisição não seja PATCH
        elif request != "PATCH":
            validation_errors['nome_comp'] = f'Campo obrigatório.'

        # Verifica se o campo num_semestre está dentro do corpo da requisição, se sim, chama a sua função de validação
        if 'num_semestre' in componente:
            semestre = self.validate_semestre_componente(componente.get("num_semestre"), componente.get("obrigatorio"))
            if semestre:
                validation_errors['num_semestre'] = semestre
        # Senão, informa que o campo é obrigatório caso a requisição não seja PATCH
        elif request != "PATCH":
            validation_errors['num_semestre'] = f'Campo obrigatório.'

        # Verifica se o campo carga_horario está dentro do corpo da requisição, se sim, chama a sua função de validação
        if 'carga_horaria' in componente:
            carga = self.validate_carga_componente(componente.get("carga_horaria"))
            if carga:
                validation_errors['carga_horaria'] = carga
        # Senão, informa que o campo é obrigatório caso a requisição não seja PATCH
        elif request != "PATCH":
            validation_errors['carga_horaria'] = f'Campo obrigatório.'

        # Verifica se o campo departamento está dentro do corpo da requisição, se sim, chama a sua função de validação
        if 'departamento' in componente:
            departamento = self.validate_departamento(componente.get("departamento"))
            if departamento:
                validation_errors['departamento'] = departamento
        # Senão, informa que o campo é obrigatório caso a requisição não seja PATCH
        elif request != "PATCH":
            validation_errors['departamento'] = f'Campo obrigatório.'

        return validation_errors

    def perform_create_or_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)

    # Função responsável por tratar solicitações GET de um objeto específico.
    def retrieve(self, request, *args, **kwargs):
        try:
            componente = self.queryset.get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist:
            errors = {f'Componente Curricular não encontrado!'}
            return Response(data=errors, status=400)

        serializer = self.get_serializer(componente)
        return Response(serializer.data)

    # Função responsável por tratar solicitações POST para criação de um novo objeto de componente curricular.
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'num_semestre' not in data:
            data['num_semestre'] = 0

        if 'obrigatorio' not in data:
            data['obrigatorio'] = False

        validation_errors = self.validate_componente(data)
        if validation_errors:
            return Response(data=validation_errors, status=400)

        serializer = ComponenteCurricularSerializer(data=data)
        return self.perform_create_or_update(serializer)

    # Função responsável por tratar solicitações PUT para atualizar completamente um componente curricular.
    def update(self, request, *args, **kwargs):
        componente = self.get_object()
        data = request.data

        validation_errors = self.validate_componente(data, request.method)
        if validation_errors:
            return Response(data=validation_errors, status=400)

        if 'codigo' not in data:
            data['codigo'] = kwargs.get('pk')

        serializer = ComponenteCurricularSerializer(componente, data=data)
        return self.perform_create_or_update(serializer)


# View que está mostrando todos os objetos \criados de Professor
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('nome_prof')
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            professor = self.queryset.get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({"detail": "Professor(a) não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(professor)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if not self.queryset:
            return Response({"detail": "Nenhum professor(a) foi encontrado."}, status=status.HTTP_200_OK)

        serializer = ProfessorSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProfessorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            professor = self.get_object()
            serializer = ProfessorSerializer(professor, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Professor(a) não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        try:
            professor = self.get_object()
            serializer = ProfessorSerializer(professor, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Professor(a) não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            professor = self.queryset.get(pk=kwargs.get('pk'))
            professor.delete()
        except ObjectDoesNotExist:
            return Response({"detail": "Professor(a) não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Professor(a) excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)


# View que está mostrando todos os objetos criados de Turma
class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurmaSerializerFormatado

        return TurmaSerializer

    def split_horarios(self, horario):
        vetor_horarios = set(horario.split())

        for index, horario in enumerate(list(vetor_horarios)):
            if re.match(r'^[2-7]+[MmTtNn][1-6]+$', horario):
                # Verifica se a possibilidade de quebrar o horá\rio em partes menores
                if len(horario) > 3:
                    dias = "".join(sorted(re.sub(r'[MmNnTt].*', '', horario)))
                    turno = re.search(r'[MmNnTt]', horario).group()
                    horas = "".join(sorted(re.sub(r'^.*[MmNnTt]', '', horario)))

                    for dia in list(dias):
                        for hora in list(horas):
                            aux_horario = dia + turno + hora
                            vetor_horarios.add(aux_horario)

                    vetor_horarios.remove(horario)

        return " ".join(vetor_horarios)

    def validate_codigo_turma(self, codigo):
        if not re.match(r'^([A-Z]{3})([0-9]{4})$', codigo):
            return f"Formato inválido do código ({codigo})."

        componente = ComponenteCurricular.objects.filter(codigo=codigo).first()
        if not componente:
            return f"Não existe componente curricular com esse código ({codigo})."

    def validate_numero_turma(self, codigo, num_turma):
        if not num_turma:
            return f'É necessário informar o número da turma.'

        try:
            num_turma = int(num_turma)
        except ValueError:
            return f"O campo de número da turma deve conter apenas números inteiros."

        if num_turma < 1:
            return f"O número da turma ({num_turma}) deve maior que 0."

        turma = Turma.objects.filter(cod_componente=codigo, num_turma=num_turma)
        if turma.exists():
            return f"Já existe uma turma com esse código e número ({codigo} - {num_turma})."

    def validate_horario_turma(self, horarios, carga_horaria):
        vetor_horarios = list(set(horarios.split()))
        contador_h = 0

        # Verifica se o horário está dentro do limite para a carga horária do componente
        if not len(vetor_horarios) == carga_horaria / 15:
            return f'O horário ({horarios}) não corresponde a carga horária da turma.'

        for index in range(len(vetor_horarios)):
            # Verifica se o horário está seguindo a sua expressão regular ou seu modelo
            if not re.match(r'^[2-7]+[MmTtNn][1-6]+$', vetor_horarios[index]):
                return f'Formato inválido do horário ({vetor_horarios[index]}).'

            # Verifica se o horário está seguindo a sua expressão regular ou seu modelo
            if not re.match(r'^[2-7]+[MmTtNn][1-6]+$', vetor_horarios[index]):
                return f'Formato inválido do horário ({vetor_horarios[index]}).'

            # Ordena de forma crescente as partes contendo número na expressão
            dias = "".join(re.sub(r'[MmNnTt].*', '', vetor_horarios[index]))
            horas = "".join(re.sub(r'^.*[MmNnTt]', '', vetor_horarios[index]))

            # Verifica se nas partes contendo números, contém apenas números
            if re.search(r'[a-zA-Z]', dias) or re.search(r'[a-zA-Z]', horas):
                return f'Formato inválido do horário ({vetor_horarios[index]}).'

            # Incrementa a quantidade de horas no horario no contador_h
            contador_h += len(dias) * len(horas)

            turno = (re.search(r'[MmNnTt]', vetor_horarios[index])).group().upper()

            # Após as informações serem ordenadas e verificadas, são postas na string novamente
            vetor_horarios[index] = dias + turno + horas

        # Verifica se a quantidade de horas presente no horário está correto
        if not contador_h == carga_horaria / 15:
            return f'A quantidade de horas no horário está inválida ({contador_h} - {carga_horaria}).'

    def validate_vagas_turma(self, num_vagas):
        try:
            num_vagas = int(num_vagas)
        except ValueError:
            return f"O campo de número de vagas deve conter apenas números inteiros."

        if num_vagas < 0:
            return f"O número de vagas ({num_vagas}) deve ser positivo."

    def validate_professores_turma(self, codigo, professores):
        for id_professor in professores:
            professor = Professor.objects.get(pk=id_professor)
            componente = ComponenteCurricular.objects.filter(codigo=codigo).first()

            if componente:
                if (professor.horas_semanais + Decimal(componente.carga_horaria / 15)) > 20:
                    return f"Quantidade máxima de horas semanais do professor ({professor}) alcançada."

    def validate_turma(self, turma, id_turma=0, request=""):
        validation_errors = {}

        aux_turma = None
        is_equal_num_turma = False
        if int(id_turma) != 0:
            aux_turma = self.queryset.get(pk=id_turma)
            if turma.get("num_turma") == aux_turma.num_turma:
                is_equal_num_turma = True

        if 'cod_componente' in turma:
            cod_componente = self.validate_codigo_turma(turma.get("cod_componente").upper())
            if cod_componente:
                validation_errors['cod_componente'] = cod_componente
        elif request != "PATCH":
            validation_errors['cod_componente'] = f'Campo obrigatório.'

        if 'num_turma' in turma:
            if 'cod_componente' in turma and not is_equal_num_turma:
                num_turma = self.validate_numero_turma(turma.get("cod_componente"), turma.get("num_turma"))
                if num_turma:
                    validation_errors['num_turma'] = num_turma
        elif request != "PATCH":
            validation_errors['num_turma'] = f'Campo obrigatório.'

        if 'horario' in turma:
            componente = ComponenteCurricular.objects.filter(codigo=turma.get("cod_componente")).first()
            if componente:
                horario = self.validate_horario_turma(turma.get("horario").upper(), componente.carga_horaria)
                if horario:
                    validation_errors['horario'] = horario
        elif request != "PATCH":
            validation_errors['horario'] = f'Campo obrigatório.'

        if 'num_vagas' in turma:
            vagas = self.validate_vagas_turma(turma.get("num_vagas"))
            if vagas:
                validation_errors['num_vagas'] = vagas
        # elif request != "PATCH":
            # validation_errors['num_vagas'] = f'Campo obrigatório.'

        if 'professor' in turma:
            try:
                professores = turma.get("professor")

                if aux_turma:
                    professores_aux = list(aux_turma.professor.values_list('id', flat=True))
                    professores = [prof for prof in professores if prof not in professores_aux]

                if professores:
                    professor = self.validate_professores_turma(turma.get("cod_componente"), professores)
                    if professor:
                        validation_errors['professor'] = professor
            except ObjectDoesNotExist:
                pass

        return validation_errors

    def perform_create_or_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)

    def retrieve(self, request, *args, **kwargs):
        try:
            turma = self.queryset.get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist:
            errors = {"Turma não encontrado!"}
            return Response(data=errors, status=400)

        serializer = self.get_serializer(turma)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'horario' in data:
            data['horario'] = self.split_horarios(data.get("horario"))

        if 'num_vagas' in data:
            if not data.get("num_vagas"):
                data['num_vagas'] = 0

        validation_errors = self.validate_turma(data)
        if validation_errors:
            return Response(data=validation_errors, status=400)

        serializer = TurmaSerializer(data=data)
        return self.perform_create_or_update(serializer)

    def update(self, request, *args, **kwargs):
        turma = self.get_object()
        data = request.data.copy()

        if 'horario' in data:
            data['horario'] = self.split_horarios(data.get("horario"))

        if 'cod_componente' not in data:
            data['cod_componente'] = turma.cod_componente.codigo

        validation_errors = self.validate_turma(data, kwargs.get('pk'), request.method)
        if validation_errors:
            return Response(data=validation_errors, status=400)

        serializer = TurmaSerializer(turma, data=data)
        return self.perform_create_or_update(serializer)


# APIView que mostra todos os horários de Turmas com mesmo componentes
class ListaHorariosComponente(generics.ListAPIView):
    def get_queryset(self):  # Realiza a busca dos componentes e retorna as turmas desses componentes
        query_set_turmas = Turma.objects.filter(cod_componente=self.kwargs['cod'])
        return query_set_turmas

    serializer_class = HorariosSerializer
    permission_classes = [IsAuthenticated]


# APIView que mostra todos os horários de Turmas com componente de mesmo semestre
class ListaHorariosSemestre(generics.ListAPIView):
    def get_queryset(self):  # Realiza a busca dos componentes por semestre e retorna as turmas desses componentes
        query_set_componenetes = ComponenteCurricular.objects.filter(num_semestre=self.kwargs['semestre']).values(
            'codigo')
        query_set_turmas = Turma.objects.filter(cod_componente__in=query_set_componenetes)

        return query_set_turmas

    serializer_class = HorariosSerializer
    permission_classes = [IsAuthenticated]


# APIView que mostra todos os horários de Turmas de mesmo professor
class ListaHorariosProfessor(generics.ListAPIView):
    def get_queryset(self):  # Realiza a busca do professor e retorna as turmas desses professor
        query_set_turmas = Turma.objects.filter(professor=self.kwargs['pk'])
        return query_set_turmas

    serializer_class = HorariosSerializer
    permission_classes = [IsAuthenticated]


class ListaHorariosConflito(generics.ListAPIView):
    def get_queryset(self):
        turms_ign = []  # Irá armazenar os id das turmas que vão ser ignoradas na busca
        comps_ign = []  # Irá armazenar os códigos dos componentes que vão ser ignoradas na busca

        conflitos = set()
        turmas = list(Turma.objects.all())

        # Pecorre todas as turmas cadastradas
        for turma in turmas:
            turms_ign.append(turma.id)
            comps_ign.append(turma.cod_componente)

            # Realiza a busca do semestre do componente da turma e de todos os componentes desse semestre
            componenete = ComponenteCurricular.objects.get(codigo=turma.cod_componente.codigo)
            componenetes_sems = ComponenteCurricular.objects.filter(num_semestre=componenete.num_semestre). \
                values('codigo')

            # Realiza a busca das turmas dos componentes que possui mesmo semestre do componente da turma
            turmas_sems = Turma.objects.filter(cod_componente__in=componenetes_sems).exclude(
                cod_componente__in=comps_ign)

            # Separa todos os horários da string
            horarios1 = turma.horario.split()

            # Pecorre todas as turmas resultado da busca por semestre
            for aux_turma_sems in turmas_sems:
                horarios2 = aux_turma_sems.horario.split()
                horarios_conflit = set()

                # Bloco de código faz a comparação de todos os horários
                for aux_horario1 in horarios1:
                    for aux_horario2 in horarios2:
                        if (turma.id != aux_turma_sems.id) and (turma.cod_componente != aux_turma_sems.cod_componente) \
                                and (aux_horario1 == aux_horario2):
                            horarios_conflit.add(aux_horario1)
                            horarios_conflit.add(aux_horario2)

                # Verifica houve conflito entre os horários comparados
                if len(horarios_conflit) != 0:
                    conflito = (turma, aux_turma_sems, " ".join(horarios_conflit), "Por semestre")
                    conflitos.add(conflito)

            # Realiza a busca das turmas de todos os professores presente na turma
            turmas_prof = Turma.objects.filter(professor__in=turma.professor.all()).exclude(id__in=turms_ign)

            # Pecorre todas as turmas resultado da busca por professor
            for aux_turma_prof in turmas_prof:
                horarios2 = aux_turma_prof.horario.split()
                horarios_conflit = set()

                # Bloco de código faz a comparação de todos os horários
                for aux_horario1 in horarios1:
                    for aux_horario2 in horarios2:
                        if (turma.id != aux_turma_prof.id) and (turma.cod_componente != aux_turma_prof.cod_componente) \
                                and (aux_horario1 == aux_horario2):
                            horarios_conflit.add(aux_horario1)
                            horarios_conflit.add(aux_horario2)

                # Verifica houve conflito entre os horários comparados
                if len(horarios_conflit) != 0:
                    conflito = (turma, aux_turma_prof, " ".join(horarios_conflit), "Por professor")
                    conflitos.add(conflito)

        return conflitos

    serializer_class = ConflitosSerializer
    permission_classes = [IsAuthenticated]
