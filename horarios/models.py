from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class ComponenteCurricular(models.Model):
    codigo = models.CharField(primary_key=True, max_length=7)
    nome = models.CharField(max_length=80)
    num_semestre = models.IntegerField()
    carga_horaria = models.IntegerField()
    departamento = models.CharField(max_length=80)
    obrigatorio = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nome.upper())


class Turma(models.Model):
    cod_componente = models.ForeignKey(ComponenteCurricular, related_name='turma_disciplina', on_delete=models.CASCADE)
    num_turma = models.PositiveSmallIntegerField()
    horario = models.CharField(max_length=15)
    professor = models.ManyToManyField("Professor", related_name='turma_professor', null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cod_componente', 'num_turma'], name='unique_cod_componente_num_turma'),
        ]

    def __str__(self):
        return "{} - Turma {}".format(self.cod_componente, self.num_turma)


class Professor(models.Model):
    nome_prof = models.CharField(max_length=80)
    horas_semanais = models.IntegerField(default=0)
    turmas = models.ManyToManyField("Turma", related_name='professor_turma', null=True, blank=True)

    def __str__(self):
        return self.nome_prof
