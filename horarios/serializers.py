from .models import ComponenteCurricular, Professor, Turma
from rest_framework import serializers


class ComponenteCurricularSerializer(serializers.HyperlinkedModelSerializer):
    ##obrigatorio = serializers.SerializerMethodField()

    class Meta:
        model = ComponenteCurricular
        fields = ['url', 'codigo', 'nome', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio']

    ##def get_obrigatorio(self, componente):
        ##return 'Obrigatorio' if componente.obrigatorio else 'Opcional'


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['url', 'nome_prof', 'horas_semanais', 'turmas']


class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    ##professor_turma = ProfessorSerializer(many=True)

    class Meta:
        model = Turma
        fields = ['url', 'cod_componente', 'num_turma', 'horario', 'professor_turma']


class ListaTurmasProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['cod_componente', 'num_turma', 'horario', 'professor_turma']


class ListaTurmaComponenteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['cod_componente', 'num_turma', 'horario', 'professor_turma']


class ListaTurmaSemestreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['cod_componente', 'num_turma', 'horario']