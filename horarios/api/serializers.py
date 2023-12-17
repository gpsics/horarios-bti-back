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


# Serializer dos dados de uma Turma simplificado
class TurmaSerializerSimplificado(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma']


# Serializer dos dados de uma Turma com o horário formatado
class TurmaSerializerFormatado(serializers.ModelSerializer):
    horario = serializers.SerializerMethodField('get_horario')

    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor']

    def get_horario(self, Turma):
        def estruturar_horario(horarios, recursive=True):
            vetor_horarios = []
            tokenize_horarios = horarios.split()
            model = r'^(\d+)([MTN])(\d+)$'

            # Percorre o vetor para realizar a comparação
            for horario in tokenize_horarios:
                changed = False

                # Verifica se vetor está vazio
                if vetor_horarios:
                    # Percorre o vetor para realizar a comparação
                    for index_temp, horario_temp in enumerate(vetor_horarios):
                        if horario != horario_temp and not changed:
                            # Separação dos termos do horário formatado
                            match1 = re.match(model, horario_temp)
                            dia1 = "".join(match1[1])
                            turno1 = "".join(match1[2])
                            hora1 = "".join(match1[3])

                            # Separação dos termos do horário a ser comparado
                            match2 = re.match(model, horario)
                            dia2 = "".join(match2[1])
                            turno2 = "".join(match2[2])
                            hora2 = "".join(match2[3])

                            # Primeiramente compara se os horários estão no mesmo turno
                            if turno1 == turno2:
                                # Compara se as horas são iguais
                                if hora1 == hora2:
                                    # Junta os termos que representa os dias dos horários
                                    dia1 = "".join(sorted(match1[1] + match2[1]))
                                    changed = True

                                # Compara se os dias são iguais
                                if dia1 == dia2:
                                    # Junta os termos que representa as horas dos horários
                                    hora1 = "".join(sorted(match1[3] + match2[3]))
                                    changed = True

                                # Verifica se houve junção dos termos dos horários comparados
                                if not changed and (index_temp + 1) == len(vetor_horarios):
                                    # Se não houver mudança, o horário já é adicionado no vetor
                                    vetor_horarios.append(horario)
                                else:
                                    # Se houver mudança, o horário é modificado no vetor
                                    vetor_horarios[index_temp] = dia1 + turno1 + hora1

                            elif (index_temp + 1) == len(vetor_horarios):
                                # Se os horários tiveram turnos diferentes, o horário é adicionado no vetor
                                vetor_horarios.append(horario)
                else:
                    # Se o vetor estiver vazio, o horário já é adicionado no vetor
                    vetor_horarios.append(horario)

            # Se a opção 'recursive' for True, a função é chamada novamente
            if recursive:
                vetor_horarios = estruturar_horario(" ".join(vetor_horarios), False)

            # Retorna o vetor dos horários
            return vetor_horarios

        # Retorna o horário formatado em uma String
        return " ".join(estruturar_horario(Turma.horario))


# Serializer dos dados de uma Turma (Simplificação da informação para exibir os horários)
class HorariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario']


# Serializer dos dados de um Conflito de Turmas
class ConflitosSerializer(serializers.Serializer):
    turma1 = TurmaSerializerSimplificado
    turma2 = TurmaSerializerSimplificado
    horario = serializers.CharField()
    conflito = serializers.CharField()

    # Método responsável por serelializar o objeto
    def to_representation(self, instance):
        return {
            'turma1': TurmaSerializerSimplificado(instance[0]).data,
            'turma2': TurmaSerializerSimplificado(instance[1]).data,
            'horario': instance[2],
            'conflito': instance[3],
        }
