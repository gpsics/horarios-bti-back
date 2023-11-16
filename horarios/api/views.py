from rest_framework import viewsets, generics
from .serializers import ComponenteCurricularSerializer, ProfessorSerializer, TurmaSerializer, \
    TurmaSerializerFormatado, HorariosSerializer, ConflitosSerializer
from horarios.models import ComponenteCurricular, Professor, Turma

from rest_framework.permissions import IsAuthenticated


# View que está mostrando todos os objetos criados de Componente Curricular
class ComponenteCurricularViewSet(viewsets.ModelViewSet):
    queryset = ComponenteCurricular.objects.all()
    serializer_class = ComponenteCurricularSerializer
    permission_classes = [IsAuthenticated]


# View que está mostrando todos os objetos criados de Professor
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]


# View que está mostrando todos os objetos criados de Turma
class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TurmaSerializerFormatado

        return TurmaSerializer


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
        conflitos = set()
        turmas = list(Turma.objects.all())

        for turma in turmas:
            componenete = ComponenteCurricular.objects.get(codigo=turma.cod_componente.codigo)
            componenetes_sems = ComponenteCurricular.objects.filter(num_semestre=componenete.num_semestre).\
                values('codigo')

            turmas_sems = Turma.objects.filter(cod_componente__in=componenetes_sems).exclude(cod_componente=turma.cod_componente)
            horarios1 = turma.horario.split()

            for aux_turma_sems in turmas_sems:
                horarios2 = aux_turma_sems.horario.split()

                for aux_horario1 in horarios1:
                    for aux_horario2 in horarios2:
                        if (turma.id != aux_turma_sems.id) and (turma.cod_componente != aux_turma_sems.cod_componente) \
                                and (aux_horario1 == aux_horario2):
                            conflito = (turma, aux_turma_sems, aux_horario1, "Conflito - Semestre")
                            conflitos.add(conflito)

            turmas_prof = Turma.objects.filter(professor__in=turma.professor.all()).exclude(id=turma.id)

            for aux_turma_prof in turmas_prof:
                horarios2 = aux_turma_prof.horario.split()

                for aux_horario1 in horarios1:
                    for aux_horario2 in horarios2:
                        if (turma.id != aux_turma_prof.id) and (turma.cod_componente != aux_turma_prof.cod_componente) \
                                and (aux_horario1 == aux_horario2):
                            conflito = (turma, aux_turma_prof, aux_horario1, "Conflito - Professor")
                            conflitos.add(conflito)

            turmas.pop(0)

        return conflitos

    serializer_class = ConflitosSerializer
    permission_classes = [IsAuthenticated]

