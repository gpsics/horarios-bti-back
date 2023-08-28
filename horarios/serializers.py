from .models import ComponenteCurricular, Professor, Turma
from rest_framework import serializers


# Classe serializadora de Componente Curricular
class ComponenteCurricularSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponenteCurricular
        fields = ['codigo', 'nome', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio', 'url']


# Classe serializadora de Turma
class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['cod_componente', 'num_turma', 'horario', 'professor', 'url']


# Classe serializadora de Professor
class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome_prof', 'horas_semanais', 'url']

