from ..models import ComponenteCurricular, Professor, Turma
from ..services import ComponenteCurricularService
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
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
    codigo = serializers.CharField(
        required=True,
        max_length=7,
        min_length=7,
        error_messages={'codigo': 'É necessário informar o código do componente curricular.'})

    nome_comp = serializers.CharField(
        required=True,
        allow_blank=True,
        error_messages={'nome_comp': 'É necessário informar o nome do componente curricular.'})

    num_semestre = serializers.IntegerField(
        required=True,
        error_messages={'num_semestre': 'É necessário informar o número do semestre do componente curricular.'})

    obrigatorio = serializers.BooleanField(
        required=False,
        default=False)

    carga_horaria = serializers.DecimalField(
        required=True,
        max_digits=4,
        decimal_places=0,
        error_messages={'carga_horaria': 'É necessário informar a carga horária do componente curricular.'})

    departamento = serializers.ChoiceField(
        required=True,
        choices=ComponenteCurricular.DEPARTAMENTO,
        error_messages={
            'required': 'É necessário informar o departamento do componente curricular',
            'invalid_choice': 'É necessário escolher uma opção válida para o departamento.'
        })

    class Meta:
        model = ComponenteCurricular
        fields = ['codigo', 'nome_comp', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio']

    def validate(self, data):
        errors = ComponenteCurricularService.validate_semestre_obrigatorio(data.get('num_semestre'), data.get('obrigatorio'))
        if errors:
            raise serializers.ValidationError(errors)

        return data

    # Função para validar o código de um componente curricular
    def validate_codigo(self, codigo):
        # Verifica se o código não está vázio
        if not codigo:
            raise serializers.ValidationError("É necessário informar o código do componente.")

        # Verifica se o código possui o tamanho correto
        if len(codigo) != 7:
            raise serializers.ValidationError("O código do componente deve ter 7 caracteres alfanuméricos.")

        # Verifica se o código está no formato correto com uso de regex (Ex. LLL0000)
        if not re.match(r'^([A-Z]{3})([0-9]{4})$', codigo):
            raise serializers.ValidationError(f"Formato inválido do código ({codigo}).")

        # Verifica se o código passado corresponde a um componente já existente
        try:
            componente = ComponenteCurricular.objects.get(pk=codigo)
            if componente:
                raise serializers.ValidationError(f"Já existe um componente com esse código ({codigo}).")
        except ObjectDoesNotExist:
            pass

    # Função para validar o nome de um componente curricular
    def validate_nome_comp(self, nome):
        # Verifica se o nome do componente contém pelo menos um caractere
        if not nome:
            raise serializers.ValidationError("O nome do componente deve ser informado.")

        # Verifica se o campo nome do componente é uma String
        if not isinstance(nome, str):
            raise serializers.ValidationError("O campo de nome do componente deve ser uma String.")

        # Verifica se o nome do componente contém pelo menos um caractere
        if len(nome) > 80:
            raise serializers.ValidationError("O nome do componente deve ter no máximo 80 caracteres.")

        # Verifica se o nome do componente contém apenas letras e espaços, nada de caracteres especiais
        padrao = re.compile(r'[a-zA-ZÀ-ú\s]+')
        if not padrao.fullmatch(nome):
            raise serializers.ValidationError("O nome do componente deve conter apenas letras e espaços.")

        return nome

    def validate_obrigatorio(self, obrigatorio):
        # Verifica se o campo obrigatório é do tipo Boolean
        if not isinstance(obrigatorio, bool):
            raise serializers.ValidationError("O campo obrigatório deve ter um valor booleano (True ou False).")

        return obrigatorio

    # Função para validar o número do semestre de um componente curricular
    def validate_num_semestre(self, semestre):
        try:
            semestre = int(semestre)
        except ValueError:
            raise serializers.ValidationError("O campo de número de semestre deve ser um número inteiro.")

        # Verifica se o semestre é um número menor que 0
        if semestre < 0:
            raise serializers.ValidationError(f"O número do semestre ({semestre}) deve ser maior ou igual a 0.")

        # Verifica se o semestre é um número maior que 6
        if semestre > 6:
            raise serializers.ValidationError(f"O número do semestre ({semestre}) deve ser menor ou igual a 6.")

        return semestre

    # Função para validar a carga horária de um componente curricular
    def validate_carga_horaria(self, carga):
        try:
            carga = int(carga)
        except ValueError:
            raise serializers.ValidationError("O campo da carga horário deve ser um número inteiro.")

        # Verifica se a carga horária do componente é divisível por 15 e maior que 0
        if carga < 0 or not carga % 15 == 0:
            raise serializers.ValidationError(f"Carga horária ({carga}) deve maior que 0 e divisível por 15.")

        return carga


# Serializer dos dados de um Professor
class ProfessorSerializer(serializers.ModelSerializer):
    nome_prof = serializers.CharField(
        required=True,
        allow_blank=True,
        error_messages={'nome_prof': 'É necessário informar o nome do professor(a).'}
    )

    class Meta:
        model = Professor
        fields = ['id', 'nome_prof', 'horas_semanais']  # 'url'

    def validate_nome_prof(self, nome):
        if not nome:
            raise serializers.ValidationError("O nome do professor deve ser informado.")

        nome = re.sub(r'\s+', ' ', nome).upper().strip()

        if len(nome) > 80:
            raise serializers.ValidationError("O nome do professor deve ter no máximo 80 caracteres.")

        padrao = re.compile(r'[a-zA-ZÀ-ú\s]+')
        if not padrao.fullmatch(nome):
            raise serializers.ValidationError("O nome do professor deve conter apenas letras e espaços.")

        professores = Professor.objects.filter(nome_prof=nome)
        if professores.exists():
            raise serializers.ValidationError("Já existe um professor com o nome {nome}.")

        return nome


# Serializer dos dados de uma Turma
class TurmaSerializer(serializers.ModelSerializer):
    num_vagas = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor']


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
    turma1 = HorariosSerializer
    turma2 = HorariosSerializer
    horario = serializers.CharField()
    conflito = serializers.CharField()

    # Método responsável por serelializar o objeto
    def to_representation(self, instance):
        return {
            'turma1': HorariosSerializer(instance[0]).data,
            'turma2': HorariosSerializer(instance[1]).data,
            'horario': instance[2],
            'conflito': instance[3],
        }
