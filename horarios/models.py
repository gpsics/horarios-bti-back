from django.db import models
from django.db.models.signals import post_save, m2m_changed
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
    horas_semanais = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    turmas = models.ManyToManyField("Turma", related_name='professor_turma', null=True, blank=True)

    def __str__(self):
        return self.nome_prof

def calcular_horas(instance):
    horas = 0
    for turmas in instance.turmas.all():
        horas += turmas.cod_componente.carga_horaria / 15
    instance.horas_semanais = horas
    instance.save()


@receiver(post_save, sender=Professor)
def calcular_horas_criacao(sender, instance, created, **kwargs):
    if created:
        calcular_horas(instance)


@receiver(m2m_changed, sender=Professor.turmas.through)
def calcular_horas_alteracao(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        calcular_horas(instance)

