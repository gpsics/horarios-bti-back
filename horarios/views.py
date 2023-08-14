from rest_framework import viewsets, generics
from rest_framework import permissions, authentication
from .serializers import ComponenteCurricularSerializer, ProfessorSerializer, TurmaSerializer, ListaTurmasProfessorSerializer, ListaTurmaComponenteSerializer
from .models import ComponenteCurricular, Professor, Turma


class ComponenteCurricularViewSet(viewsets.ModelViewSet):
    queryset = ComponenteCurricular.objects.all()
    serializer_class = ComponenteCurricularSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


class ListaTurmasProfessor(generics.ListAPIView):
    def get_queryset(self):
        query_set = Turma.objects.filter(professor_turma=self.kwargs['pk'])
        return query_set

    serializer_class = ListaTurmasProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


class ListaTurmasComponente(generics.ListAPIView):
    def get_queryset(self):
        query_set = Turma.objects.filter(cod_componente=self.kwargs['pk'])
        return query_set

    serializer_class = ListaTurmaComponenteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

