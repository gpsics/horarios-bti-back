from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema_field, extend_schema
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import re

from ..models import ComponenteCurricular, Professor, Turma
from ..services import TurmaService


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
        validators=[UniqueValidator(queryset=ComponenteCurricular.objects.all(), lookup="iexact",
                                    message="Já existe um componente com esse código.")],
        error_messages={'required': 'É necessário informar o código do componente curricular.'})

    nome_comp = serializers.CharField(
        required=True,
        allow_blank=True,
        max_length=80,
        error_messages={'required': 'É necessário informar o nome do componente curricular.',
                        'max_length': 'O nome do componente deve ter no máximo 80 caracteres'})

    num_semestre = serializers.IntegerField(
        required=True,
        error_messages={'required': 'É necessário informar o número do semestre do componente curricular.',
                        'invalid': 'Valor inválido. Informe um valor inteiro válido.'})

    obrigatorio = serializers.BooleanField(
        required=False,
        default=False,
        error_messages={'invalid': 'O valor inválido. Informe um valor booleano (true/false).'})

    carga_horaria = serializers.DecimalField(
        required=True,
        max_digits=4,
        decimal_places=0,
        error_messages={'required': 'É necessário informar a carga horária do componente curricular.',
                        'invalid': 'Valor inválido. Informe um valor inteiro válido.'})

    departamento = serializers.ChoiceField(
        required=True,
        choices=ComponenteCurricular.DEPARTAMENTO,
        error_messages={'required': 'É necessário informar o departamento do componente curricular',
                        'invalid_choice': 'É necessário escolher uma opção válida para o departamento.'})

    class Meta:
        model = ComponenteCurricular
        fields = ['codigo', 'nome_comp', 'num_semestre', 'carga_horaria', 'departamento', 'obrigatorio']

    # Validações compostas do componente curricular
    def validate(self, data):
        if 'num_semestre' in data:
            # Verifica se o componenete é obrigatório e se está com o número de semestre é igual a 0
            if data['num_semestre'] == 0 and data['obrigatorio']:
                raise serializers.ValidationError({"num_semestre": "O componente quando obrigatório deve possuir um "
                                                                       "semestre diferente de 0."})

        return data

    # Validação do código dos componentes curriculares
    def validate_codigo(self, codigo):
        # Verifica se o código possui o tamanho correto
        if len(codigo) != 7:
            raise serializers.ValidationError("O código do componente deve ter 7 caracteres alfanuméricos.")

        # Verifica se o código está no formato correto (Ex. LLL0000)
        if not re.match(r'^([A-Z]{3})([0-9]{4})$', codigo.upper()):
            raise serializers.ValidationError(f"Formato inválido do código ({codigo}).")

        return str(codigo).upper()

    # Validação do nome dos componentes curriculares
    def validate_nome_comp(self, nome):
        # Verifica se o nome do componente contém pelo menos um caractere
        if len(nome) > 80:
            raise serializers.ValidationError("O nome do componente deve ter no máximo 80 caracteres.")

        # Verifica se o nome do componente contém apenas letras e espaços, nada de caracteres especiais
        padrao = re.compile(r'[a-zA-ZÀ-ú\s]+')
        if not padrao.fullmatch(nome):
            raise serializers.ValidationError("O nome do componente deve conter apenas letras e espaços.")

        return str(nome).upper()

    # Validação do número do semestre dos componentes curriculares
    def validate_num_semestre(self, semestre):
        # Verifica se o semestre é um número menor que 0
        if semestre < 0:
            raise serializers.ValidationError(f"O número do semestre ({semestre}) deve ser maior ou igual a 0.")

        # Verifica se o semestre é um número maior que 6
        if semestre > 6:
            raise serializers.ValidationError(f"O número do semestre ({semestre}) deve ser menor ou igual a 6.")

        return semestre

    # Validação da carga horária dos componentes curriculares
    def validate_carga_horaria(self, carga):
        # Verifica se a carga horária do componente é divisível por 15 e maior que 0
        if carga < 0 or not carga % 15 == 0:
            raise serializers.ValidationError(f"Carga horária ({carga}) deve maior que 0 e divisível por 15.")

        return carga


# Serializer dos dados de um Professor
class ProfessorSerializer(serializers.ModelSerializer):
    nome_prof = serializers.CharField(
        required=True,
        allow_blank=True,
        max_length=80,
        validators=[UniqueValidator(queryset=Professor.objects.all(), lookup="iexact",
                                    message="Já existe um professor com esse nome.")],
        error_messages={'required': 'É necessário informar o nome do professor(a).',
                        'max_length': 'O nome do professor deve ter no máximo 80 caracteres.',}
    )

    class Meta:
        model = Professor
        fields = ['id', 'nome_prof', 'horas_semanais']  # 'url'

    # Validação do nome dos professores
    def validate_nome_prof(self, nome):
        nome = re.sub(r'\s+', ' ', nome).upper().strip()

        # Verifica se o nome do professor contém apenas letras e espaços, nada de caracteres especiais
        padrao = re.compile(r'[a-zA-ZÀ-ú\s]+')
        if not padrao.fullmatch(nome):
            raise serializers.ValidationError("O nome do professor deve conter apenas letras e espaços.")

        return nome


# Serializer dos dados de uma Turma
class TurmaSerializer(serializers.ModelSerializer):
    cod_componente = serializers.PrimaryKeyRelatedField(
        queryset=ComponenteCurricular.objects.all(),
        required=True,
        error_messages={'required': 'É necessário informar o componente curricular da turma.'})

    num_turma = serializers.IntegerField(
        required=True,
        error_messages={'required': 'É necessário informar o número da turma.',
                        'invalid': 'Valor inválido. Informe um valor inteiro válido.'})

    horario = serializers.CharField(
        required=True,
        max_length=80,
        error_messages={'required': 'É necessário informar o horário da turma.'})

    num_vagas = serializers.IntegerField(
        required=False,
        default=0,
        error_messages={'invalid': 'Valor inválido. Informe um valor inteiro válido.'})

    professor = serializers.PrimaryKeyRelatedField(
        queryset=Professor.objects.all(),
        many=True,
        required=False,
        error_messages={'invalid': 'Teste'})

    # Validações compostas de turmas
    def validate(self, data):
        # Validação do número das turmas
        num_turma = data.get('num_turma')
        if 'num_turma' in data:
            if num_turma < 1:
                raise serializers.ValidationError({"num_turma": f"O número da turma ({num_turma}) deve maior que 0."})

            if self.instance:
                componente = self.instance.cod_componente
                turma = Turma.objects.filter(cod_componente=componente, num_turma=num_turma).exclude(pk=self.instance.id)
            else:
                componente = data.get('cod_componente')
                turma = Turma.objects.filter(cod_componente=componente, num_turma=num_turma)

            if turma.exists():
                raise serializers.ValidationError({"num_turma": f"Já existe uma turma com esse código e número "
                                                                    f"({componente.codigo} - {num_turma})."})

        # Validação do horário das turmas
        horarios = data.get('horario')
        if 'horario' in data:
            if self.instance:
                carga_horaria = self.instance.cod_componente.carga_horaria
            else:
                carga_horaria = data.get('cod_componente').carga_horaria

            vetor_horarios = TurmaService.split_horarios(horarios)
            contador_h = 0

            # Verifica se o horário está dentro do limite para a carga horária do componente
            if not len(vetor_horarios) == carga_horaria / 15:
                raise serializers.ValidationError({"horario": f'O horário ({horarios}) não corresponde a carga horária '
                                                              f'({carga_horaria}) da turma.'})

            for index in range(len(vetor_horarios)):
                # Verifica se o horário está seguindo a sua expressão regular ou seu modelo
                if not re.match(r'^[2-7]+[MmTtNn][1-6]+$', vetor_horarios[index]):
                    raise serializers.ValidationError({"horario": f'Formato inválido do horário '
                                                                  f'({vetor_horarios[index]}).'})

                # Verifica se o horário está seguindo a sua expressão regular ou seu modelo
                if not re.match(r'^[2-7]+[MmTtNn][1-6]+$', vetor_horarios[index]):
                    raise serializers.ValidationError({"horario": f'Formato inválido do horário '
                                                                  f'({vetor_horarios[index]}).'})

                # Ordena de forma crescente as partes contendo número na expressão
                dias = "".join(re.sub(r'[MmNnTt].*', '', vetor_horarios[index]))
                horas = "".join(re.sub(r'^.*[MmNnTt]', '', vetor_horarios[index]))

                # Verifica se nas partes contendo números, contém apenas números
                if re.search(r'[a-zA-Z]', dias) or re.search(r'[a-zA-Z]', horas):
                    raise serializers.ValidationError({"horario": f'Formato inválido do horário '
                                                                  f'({vetor_horarios[index]}).'})

                # Incrementa a quantidade de horas no horario no contador_h
                contador_h += len(dias) * len(horas)

                turno = (re.search(r'[MmNnTt]', vetor_horarios[index])).group().upper()

                # Após as informações serem ordenadas e verificadas, são postas na string novamente
                vetor_horarios[index] = dias + turno + horas

            # Verifica se a quantidade de horas presente no horário está correto
            if not contador_h == carga_horaria / 15:
                raise serializers.ValidationError({"horario": f'A quantidade de horas no horário está inválida '
                                                              f'({contador_h} - {carga_horaria}).'})

            data['horario'] = " ".join(vetor_horarios)

        # Validação dos professores das turmas
        professores = data.get('professor')
        if 'professor' in data:
            for id_professor in professores:
                try:
                    professor = Professor.objects.get(pk=id_professor.id)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError({"professor": f"Professor com Id ({id_professor}) não encontrado."})

                if self.instance:
                    componente = self.instance.cod_componente
                else:
                    componente = data.get('cod_componente')

                if componente:
                    if (professor.horas_semanais + Decimal(componente.carga_horaria / 15)) > 20:
                        raise serializers.ValidationError({"professor": f"Quantidade máxima de horas semanais do "
                                                                        f"professor(a) ({professor}) alcançada."})

        return data

        # if num_turma:
        #     valid = TurmaService.validate_numero(data.get('cod_componente'), num_turma)
        #     errors = valid if (result := valid) is not None else errors
        # else:
        #     raise serializers.ValidationError(f"É necessário informar o número da turma.")

        # horario = data.get('horario')
        # if horario:
        #     valid = TurmaService.validate_horario(horario, data.get('cod_componente').carga_horaria)
        #     errors = valid if (result := valid) is not None else errors
        # else:
        #     raise serializers.ValidationError(f"É necessário informar o horário da turma.")

        # professores = data.get('professor')
        # if professores:
        #     valid = TurmaService.validate_professores(data.get('cod_componente'), professores)
        #     errors = valid if (result := valid) is not None else errors
        #
        # if errors:
        #     raise serializers.ValidationError(errors)

    # Validação do código do componente das turmas
    def validate_cod_componente(self, cod_componente):
        codigo = str(cod_componente.codigo).upper()

        if not re.match(r'^([A-Z]{3})([0-9]{4})$', codigo):
            raise serializers.ValidationError(f"Formato inválido do código ({codigo}).")

        componente = ComponenteCurricular.objects.filter(codigo=codigo).first()
        if not componente:
            raise serializers.ValidationError(f"Não existe um componente curricular com esse código ({codigo}).")

        return componente

    # Validação do número de vagas das turmas
    def validate_num_vagas(self, num_vagas):
        if num_vagas < 0:
            raise serializers.ValidationError(f"O número de vagas ({num_vagas}) deve ser positivo.")

        return num_vagas

    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor']


# Serializer dos dados de uma Turma com o horário formatado
class TurmaSerializerFormatado(serializers.ModelSerializer):
    horario = serializers.SerializerMethodField('get_horario')

    class Meta:
        model = Turma
        fields = ['id', 'cod_componente', 'num_turma', 'horario', 'num_vagas', 'professor']

    @extend_schema_field(str)
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
