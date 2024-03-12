from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

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
        serializer = TurmaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            turma = self.get_object()
            serializer = TurmaSerializer(turma, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response({"error": "Turma não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        try:
            turma = self.get_object()
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

