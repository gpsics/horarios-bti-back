from .models import ComponenteCurricular, Professor, Turma
from rest_framework import serializers


# Classe serializadora de Componente Curricular
class ComponenteCurricularSerializer(serializers.HyperlinkedModelSerializer):
    # departamento = serializers.SerializerMethodField()
    ##obrigatorio = serializers.SerializerMethodField()

    class Meta:
        model = ComponenteCurricular
        fields = ['url', 'codigo', 'nome', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio']

    ##def get_obrigatorio(self, componente):
        ##return 'Obrigatorio' if componente.obrigatorio else 'Opcional'


# Classe serializadora de Turma
class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    #professor_turma = ProfessorSerializer(many=True)

    class Meta:
        model = Turma
        fields = ['url', 'cod_componente', 'num_turma', 'horario', 'professor']


# Classe serializadora de Professor
class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    #turma_professor = TurmaSerializer(many=True)

    class Meta:
        model = Professor
        fields = ['url', 'nome_prof', 'horas_semanais']
        #fields = ['url', 'nome_prof', 'horas_semanais', 'turma_professor']

