import re

from .models import Turma, Professor, ComponenteCurricular


class TurmaService:
    @staticmethod
    def split_horarios(horario):
        vetor_horarios = set(horario.split())

        for index, horario in enumerate(list(vetor_horarios)):
            if re.match(r'^[2-7]+[MmTtNn][1-6]+$', horario):
                # Verifica se a possibilidade de quebrar o horário em partes menores
                if len(horario) > 3:
                    dias = "".join(sorted(re.sub(r'[MmNnTt].*', '', horario)))
                    turno = re.search(r'[MmNnTt]', horario).group()
                    horas = "".join(sorted(re.sub(r'^.*[MmNnTt]', '', horario)))

                    for dia in list(dias):
                        for hora in list(horas):
                            aux_horario = dia + turno + hora
                            vetor_horarios.add(aux_horario)

                    vetor_horarios.remove(horario)

        return list(sorted(vetor_horarios))

