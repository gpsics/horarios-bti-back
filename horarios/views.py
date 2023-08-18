from rest_framework import viewsets, generics
from rest_framework import permissions, authentication
from .serializers import ComponenteCurricularSerializer, ProfessorSerializer, TurmaSerializer
from .models import ComponenteCurricular, Professor, Turma


# View que está mostrando todos os objetos criados de Componente Curricular
class ComponenteCurricularViewSet(viewsets.ModelViewSet):
    # Realiza a busca de todos os objetos criados
    queryset = ComponenteCurricular.objects.all()
    # Forma de como as atributos dos objetos vão ser apresentados na tela
    serializer_class = ComponenteCurricularSerializer
    # É necessária está autenticado para conseguir as informações
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


# View que está mostrando todos os objetos criados de Professor
class ProfessorViewSet(viewsets.ModelViewSet):
    # Realiza a busca de todos os objetos criados
    queryset = Professor.objects.all()
    # Forma de como as atributos dos objetos vão ser apresentados na tela
    serializer_class = ProfessorSerializer
    # É necessária está autenticado para conseguir as informações
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


# View que está mostrando todos os objetos criados de Turma
class TurmaViewSet(viewsets.ModelViewSet):
    # Realiza a busca de todos os objetos criados
    queryset = Turma.objects.all()
    # Forma de como as atributos dos objetos vão ser apresentados na tela
    serializer_class = TurmaSerializer
    # É necessária está autenticado para conseguir as informações
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


# APIView que está mostrando os objetos de Turma de maneira personalizada
class ListaTurmasProfessor(generics.ListAPIView):
    # Função que realiza a busca que retorno os objetos de Turma com id equivalente ao da url
    def get_queryset(self):
        query_set_turmas = Turma.objects.filter(professor=self.kwargs['pk'])
        return query_set_turmas

    # Forma de como as atributos dos objetos vão ser apresentados na tela
    serializer_class = TurmaSerializer
    # É necessária está autenticado para conseguir as informações
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


# APIView que está mostrando os objetos de Turma de maneira personalizada
class ListaTurmasComponente(generics.ListAPIView):
    # Função que realiza a busca que retorno os objetos de Turma com cod equivalente ao da url
    def get_queryset(self):
        query_set_turmas = Turma.objects.filter(cod_componente=self.kwargs['cod'])
        return query_set_turmas

    # Forma de como as atributos dos objetos vão ser apresentados na tela
    serializer_class = TurmaSerializer
    # É necessária está autenticado para conseguir as informações
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]


# APIView que está mostrando os objetos de Turma de maneira personalizada
class ListaTurmasSemestre(generics.ListAPIView):
    # Função que realiza a busca e retorna os objetos de Turma com base semestre
    def get_queryset(self):
        query_set_turmas = Turma.objects.filter(cod_componente=ComponenteCurricular.objects.get(num_semestre=self.kwargs['semestre']))

        return query_set_turmas

    # Forma de como as atributos dos objetos vão ser apresentados na tela
    serializer_class = TurmaSerializer
    # É necessária está autenticado para conseguir as informações
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]

