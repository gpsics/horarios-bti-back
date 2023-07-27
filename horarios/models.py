from django.db import models

class Componente_curricular(models.Model):
    codigo = models.CharField(primary_key=True, max_length=7)
    nome = models.CharField(max_length=80)
    num_semestre = models.IntegerField()
    carga_horaria = models.IntegerField(default=0)
    departamento = models.CharField(max_length=80, null=True, blank=True)
    obrigatorio = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nome.upper())


class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    nome_prof = models.CharField(max_length=80)
    horas_semanais = models.IntegerField(default=0, blank=True)
    turmas = models.ManyToManyField("Turma", related_name='professor_turma', null=True, blank=True)

    def __str__(self):
        return self.nome_prof


class Turma(models.Model):
    cod_componente = models.ForeignKey(Componente_curricular, related_name='turma_disciplina', on_delete=models.CASCADE)
    num_turma = models.IntegerField(primary_key=True)
    horario = models.CharField(max_length=15)
    professor = models.ManyToManyField("Professor", related_name='turma_professor', null=True, blank=True)
    unique_together = ("cod_componenete", "num_turma")

    def __str__(self):
        return "{} - Turma {}".format(self.cod_componente, self.num_turma)