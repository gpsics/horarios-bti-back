from horarios.models import ComponenteCurricular, Professor, Turma
from rest_framework import serializers


# Serializer dos dados de um Componente Curricular
class ComponenteCurricularSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComponenteCurricular
        fields = ['codigo', 'nome_comp', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio']  # 'url'


# Serializer dos dados de um Professor
class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome_prof', 'horas_semanais']  # 'url'


# Serializer dos dados de uma Turma
class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    cod_componente = ComponenteCurricularSerializer()
    professor = ProfessorSerializer(many=True)

    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor']  # 'url'


# Serializer dos dados de uma Turma (Simplifica contendo apenas os horários)
class HorariosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['horario']

