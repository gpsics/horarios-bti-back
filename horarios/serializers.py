from .models import ComponenteCurricular, Professor, Turma
from rest_framework import serializers


class ComponenteCurricularSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponenteCurricular
        fields = ['codigo', 'nome', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio', 'url']


class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['cod_componente', 'num_turma', 'horario', 'professor', 'url']


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['nome_prof', 'horas_semanais', 'turmas', 'url']