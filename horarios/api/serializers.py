from horarios.models import ComponenteCurricular, Professor, Turma
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

# Serializer de customização do token JWT
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


# Serializer dos dados de um Componente Curricular
class ComponenteCurricularSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponenteCurricular
        fields = ['codigo', 'nome_comp', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio']


# Serializer dos dados de um Professor
class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome_prof', 'horas_semanais']  # 'url'


# Serializer dos dados de uma Turma
class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor']


class TurmaSerializerFormatado(serializers.ModelSerializer):
    horario = serializers.SerializerMethodField('get_horario')

    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor']

    def get_horario(self, Turma):
        vetor = []
        vetor_horarios = Turma.horario.split()
        model = r'^(\d+)([MTN])(\d+)$'

        for horario in vetor_horarios:
            if vetor:
                for index_temp, horario_temp in enumerate(vetor):
                    if horario != horario_temp:
                        # Separação dos dados do horário formatado
                        match1 = re.match(model, horario_temp)
                        dia1 = "".join(match1[1])
                        turno1 = "".join(match1[2])
                        hora1 = "".join(match1[3])

                        # Separação dos dados do horário a ser comparado
                        match2 = re.match(model, horario)
                        dia2 = "".join(match2[1])
                        turno2 = "".join(match2[2])
                        hora2 = "".join(match2[3])

                        if turno1 == turno2:
                            aux_dias = "".join(match1[1])
                            aux_horas = "".join(match1[3])
                            changed = False

                            if hora1 == hora2:
                                aux_dias = "".join(sorted(match1[1] + match2[1]))
                                changed = True

                            if dia1 == dia2 and int(hora1[-1::]) + 1 == int(hora2[-1::]):
                                aux_horas = "".join(sorted(match1[3] + match2[3]))
                                changed = True

                            if not changed and (index_temp + 1) == len(vetor):
                                vetor.append(horario)
                            else:
                                vetor[index_temp] = aux_dias + turno1 + aux_horas

                        elif (index_temp + 1) == len(vetor):
                            vetor.append(horario)
            else:
                vetor.append(horario)

        return " ".join(vetor)


# Serializer dos dados de uma Turma (Simplificação da informação para exibir os horários)
class HorariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['cod_componente', 'num_turma', 'horario']

