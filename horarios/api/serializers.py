from horarios.models import ComponenteCurricular, Professor, Turma
from rest_framework import serializers


# Classe serializadora de Componente Curricular
class ComponenteCurricularSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponenteCurricular
        fields = ['codigo', 'nome_comp', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio', 'url']


# Classe serializadora de Professor
class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome_prof', 'horas_semanais', 'url']


# Classe serializadora de Turma
class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    cod_componente = ComponenteCurricularSerializer()
    professor = ProfessorSerializer(many=True)

    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor', 'url']


# Classe serializadora de Turma
class TurmaSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'url']


class HorariosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['horario']


class TurmasConflitoSerializer(serializers.HyperlinkedModelSerializer):
    turmas = TurmaSimplesSerializer(many=True)

