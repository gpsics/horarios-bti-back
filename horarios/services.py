from .models import Turma, Professor, ComponenteCurricular
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
import re


class ComponenteCurricularService:
    @staticmethod
    def validate_semestre_obrigatorio(semestre, obrigatorio):
        # Verifica se o componente é obrigatório com semestre igual a 0
        if int(semestre) == 0 and obrigatorio:
            return {"num_semestre": "O componente quando obrigatório deve possuir um semestre diferente de 0."}


class TurmaService:
    def split_horarios(self, horario):
        vetor_horarios = set(horario.split())

        for index, horario in enumerate(list(vetor_horarios)):
            if re.match(r'^[2-7]+[MmTtNn][1-6]+$', horario):
                # Verifica se a possibilidade de quebrar o horá\rio em partes menores
                if len(horario) > 3:
                    dias = "".join(sorted(re.sub(r'[MmNnTt].*', '', horario)))
                    turno = re.search(r'[MmNnTt]', horario).group()
                    horas = "".join(sorted(re.sub(r'^.*[MmNnTt]', '', horario)))

                    for dia in list(dias):
                        for hora in list(horas):
                            aux_horario = dia + turno + hora
                            vetor_horarios.add(aux_horario)

                    vetor_horarios.remove(horario)

        return " ".join(vetor_horarios)

    @staticmethod
    def validate_numero(codigo, num_turma):
        try:
            num_turma = int(num_turma)
        except ValueError:
            return {"num_turma": "O campo de número da turma deve conter apenas números inteiros."}

        if num_turma < 1:
            return {"num_turma": f"O número da turma ({num_turma}) deve maior que 0."}

        turma = Turma.objects.filter(cod_componente=codigo, num_turma=num_turma)
        if turma.exists():
            return {"num_turma": f"Já existe uma turma com esse código e número ({codigo.codigo} - {num_turma})."}

    @staticmethod
    def validate_horario(horarios, carga_horaria):
        if not horarios:
            return {"horario": "O horário da turma deve ser informado."}

        vetor_horarios = list(set(horarios.split()))
        contador_h = 0

        # Verifica se o horário está dentro do limite para a carga horária do componente
        if not len(vetor_horarios) == carga_horaria / 15:
            return {"horario": f'O horário ({horarios}) não corresponde a carga horária ({carga_horaria}) da turma.'}

        for index in range(len(vetor_horarios)):
            # Verifica se o horário está seguindo a sua expressão regular ou seu modelo
            if not re.match(r'^[2-7]+[MmTtNn][1-6]+$', vetor_horarios[index]):
                return {"horario": f'Formato inválido do horário ({vetor_horarios[index]}).'}

            # Verifica se o horário está seguindo a sua expressão regular ou seu modelo
            if not re.match(r'^[2-7]+[MmTtNn][1-6]+$', vetor_horarios[index]):
                return {"horario": f'Formato inválido do horário ({vetor_horarios[index]}).'}

            # Ordena de forma crescente as partes contendo número na expressão
            dias = "".join(re.sub(r'[MmNnTt].*', '', vetor_horarios[index]))
            horas = "".join(re.sub(r'^.*[MmNnTt]', '', vetor_horarios[index]))

            # Verifica se nas partes contendo números, contém apenas números
            if re.search(r'[a-zA-Z]', dias) or re.search(r'[a-zA-Z]', horas):
                return {"horario": f'Formato inválido do horário ({vetor_horarios[index]}).'}

            # Incrementa a quantidade de horas no horario no contador_h
            contador_h += len(dias) * len(horas)

            turno = (re.search(r'[MmNnTt]', vetor_horarios[index])).group().upper()

            # Após as informações serem ordenadas e verificadas, são postas na string novamente
            vetor_horarios[index] = dias + turno + horas

        # Verifica se a quantidade de horas presente no horário está correto
        if not contador_h == carga_horaria / 15:
            return {"horario": f'A quantidade de horas no horário está inválida ({contador_h} - {carga_horaria}).'}

    @staticmethod
    def validate_professores(codigo, professores):
        if professores:
            for id_professor in professores:
                try:
                    professor = Professor.objects.get(pk=id_professor.id)
                except ObjectDoesNotExist:
                    return {"professor": f"Professor com Id ({id_professor}) não encontrado."}

                componente = ComponenteCurricular.objects.filter(codigo=codigo).first()

                if componente:
                    if (professor.horas_semanais + Decimal(componente.carga_horaria / 15)) > 20:
                        return {"professor": f"Quantidade máxima de horas semanais do professor(a) ({professor}) alcançada."}
