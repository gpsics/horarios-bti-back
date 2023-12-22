from rest_framework import viewsets, generics
from rest_framework.response import Response
from .serializers import ComponenteCurricularSerializer, ProfessorSerializer, TurmaSerializer, \
    TurmaSerializerFormatado, HorariosSerializer, ConflitosSerializer
from horarios.models import ComponenteCurricular, Professor, Turma

from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
import re


# View que está mostrando todos os objetos criados de Componente Curricular
class ComponenteCurricularViewSet(viewsets.ModelViewSet):
    queryset = ComponenteCurricular.objects.all()
    serializer_class = ComponenteCurricularSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data

        codigo = data.get("codigo")
        nome = data.get("nome_comp")
        semestre = data.get("num_semestre")
        carga = data.get("carga_horaria")
        obrigatorio = data.get("obrigatorio")

        if not re.match(r'^([A-Z]{3})([0-9]{4})$', codigo):
            errors = [f"Formato inválido do código ({codigo})."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        if nome == "" or len(nome) > 80:
            errors = [f"O nome do componente ({nome}) deve ter no mínimo 1 caractere e no máximo 80."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        if semestre < 0:
            errors = [f"O número do semestre ({semestre}) deve ser maior que 0."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        if semestre != 0 and not obrigatorio:
            errors = [f"O componente deve ser obrigatório quando número do semestre diferente de 0."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        if carga < 0 or not carga % 15 == 0:
            errors = [f'Carga horária ({carga}) deve maior que 0 e divisível por 15.']
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        serializer = ComponenteCurricularSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)  # Retorno com status 201 Created
        else:
            return Response(data=serializer.errors, status=400)  # Retorno com erros de validação


# View que está mostrando todos os objetos criados de Professor
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        nome = data.get("nome_prof")

        if len(nome) > 80:
            errors = ["O nome do professor deve ter no máximo 80 caracteres."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        professores = Professor.objects.filter(nome_prof=nome)
        if professores.exists():
            errors = ["O nome do professor deve ser único."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        serializer = ProfessorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)  # Retorno com status 201 Created
        else:
            return Response(data=serializer.errors, status=400)  # Retorno com erros de validação


# View que está mostrando todos os objetos criados de Turma
class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurmaSerializerFormatado

        return TurmaSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        codigo = data.get("cod_componente")
        num_turma = data.get("num_turma")
        horario = data.get("horario")
        num_vagas = data.get("num_vagas")
        professores = data.get("professor")

        if not re.match(r'^([A-Z]{3})([0-9]{4})$', codigo):
            errors = [f"Formato inválido do código ({codigo})."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        componente = ComponenteCurricular.objects.filter(codigo=codigo).first()
        if not componente:
            errors = [f"Não existe componente curricular com esse código ({codigo})."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        if num_turma < 0:
            errors = [f"O número da turma ({num_turma}) deve ser positivo."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        turma = Turma.objects.filter(cod_componente=codigo, num_turma=num_turma)
        if turma.exists():
            errors = [f"Já existe turma com esse código e número ({codigo} - {num_turma})."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        for id_professor in professores:
            professor = Professor.objects.get(pk=id_professor)

            if componente:
                if (professor.horas_semanais + Decimal(componente.carga_horaria / 15)) > 20:
                    errors = [f"Quantidade de horas semanais máxima do professor ({professor}) atinginda."]
                    return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        if num_vagas < 0:
            errors = [f"O número de vagas ({num_vagas}) deve ser positivo."]
            return Response(data=errors, status=400)  # Retorno com status 400 Bad Request

        serializer = TurmaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)  # Retorno com status 201 Created
        else:
            return Response(data=serializer.errors, status=400)  # Retorno com erros de validação


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
        turms_ign = []      # Irá armazenar os id das turmas que vão ser ignoradas na busca
        comps_ign = []      # Irá armazenar os códigos dos componentes que vão ser ignoradas na busca

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
            turmas_sems = Turma.objects.filter(cod_componente__in=componenetes_sems).exclude(cod_componente__in=comps_ign)

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
