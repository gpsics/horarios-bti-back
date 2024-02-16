from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from django.http import Http404
import re

from horarios.models import ComponenteCurricular, Professor, Turma
from .serializers import ComponenteCurricularSerializer, ProfessorSerializer, TurmaSerializer, \
    TurmaSerializerFormatado, HorariosSerializer, ConflitosSerializer


# View que está mostrando todos os objetos criados de Componente Curricular
class ComponenteCurricularViewSet(viewsets.ModelViewSet):
    serializer_class = ComponenteCurricularSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ComponenteCurricular.objects.all().order_by('nome_comp')

    def retrieve(self, request, *args, **kwargs):
        try:
            componente = self.get_queryset().get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({"detail": "Componente Curricular não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(componente)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            return Response({"detail": "Nenhum componente curricular encontrado."}, status=status.HTTP_200_OK)

        serializer = ComponenteCurricularSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ComponenteCurricularSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            componente = self.get_object()
            serializer = ComponenteCurricularSerializer(componente, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Componente curricular não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        try:
            componente = self.get_object()
            serializer = ComponenteCurricularSerializer(componente, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Componente curricular não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            componente = self.get_queryset().get(pk=kwargs.get('pk'))
            componente.delete()
        except ObjectDoesNotExist:
            return Response({"detail": "Componente curricular não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Componente curricular excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)


# View que está mostrando todos os objetos \criados de Professor
class ProfessorViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Professor.objects.all().order_by('nome_prof')

    def retrieve(self, request, *args, **kwargs):
        try:
            professor = self.get_queryset().get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({"detail": "Professor(a) não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(professor)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            return Response({"detail": "Nenhum professor(a) foi encontrado."}, status=status.HTTP_200_OK)

        serializer = ProfessorSerializer(self.get_queryset(), many=True)
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
            professor = self.get_queryset().get(pk=kwargs.get('pk'))
            professor.delete()
        except ObjectDoesNotExist:
            return Response({"detail": "Professor(a) não foi encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Professor(a) excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)


# View que está mostrando todos os objetos criados de Turma
class TurmaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Turma.objects.all()

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
            aux_turma = self.get_queryset().get(pk=id_turma)
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

    def retrieve(self, request, *args, **kwargs):
        try:
            turma = self.get_queryset().get(pk=kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({"detail": "Turma não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TurmaSerializerFormatado(turma)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if not self.get_queryset():
            return Response({"detail": "Nenhuma turma encontrada."}, status=status.HTTP_200_OK)

        serializer = TurmaSerializerFormatado(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'horario' in data:
            data['horario'] = self.split_horarios(data.get("horario"))

        validation_errors = self.validate_turma(data)
        if validation_errors:
            return Response(data=validation_errors, status=400)

        serializer = TurmaSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)
        else:
            return Response(data=serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        try:
            turma = self.get_object()
            data = request.data.copy()

            if 'horario' in data:
                data['horario'] = self.split_horarios(data.get("horario"))

            validation_errors = self.validate_turma(data, kwargs.get('pk'))
            if validation_errors:
                return Response(data=validation_errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = TurmaSerializer(turma, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Turma não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        try:
            turma = self.get_object()
            data = request.data.copy()

            if 'horario' in data:
                data['horario'] = self.split_horarios(data.get("horario"))

            validation_errors = self.validate_turma(data, kwargs.get('pk'))
            if validation_errors:
                return Response(data=validation_errors, status=status.HTTP_400_BAD_REQUEST)

            serializer = TurmaSerializer(turma, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Turma não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            turma = self.get_queryset().get(pk=kwargs.get('pk'))
            turma.delete()
        except ObjectDoesNotExist:
            return Response({"detail": "Turma não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Turma excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)


# APIView que mostra todos os horários de Turmas com mesmo componentes
class HorariosViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HorariosSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, url_path='componente', permission_classes=[IsAuthenticated])
    def horarios_comp(self, request, cod=None):
        horarios = Turma.objects.filter(cod_componente=cod)

        if horarios:
            serializer = HorariosSerializer(horarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Nenhuma turma encontrada com esse código."}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='professor', permission_classes=[IsAuthenticated])
    def horarios_prof(self, request, id_prof=None):
        horarios = Turma.objects.filter(professor=id_prof)

        if horarios:
            serializer = HorariosSerializer(horarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Nenhuma turma encontrada com esse professor."}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='semestre', permission_classes=[IsAuthenticated])
    def horarios_semestre(self, request, semestre=None):
        componenetes = ComponenteCurricular.objects.filter(num_semestre=semestre).values('codigo')
        horarios = Turma.objects.filter(cod_componente__in=componenetes)

        if horarios:
            serializer = HorariosSerializer(horarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Nenhuma turma encontrada com esse número de semestre."}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='conflitos', permission_classes=[IsAuthenticated])
    def horarios_conflitos(self, request):
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

        if conflitos:
            serializer = ConflitosSerializer(conflitos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"detail": "Nenhum conflito de horário encontrado entre as turmas."}, status=status.HTTP_200_OK)

