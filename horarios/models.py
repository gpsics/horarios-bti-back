from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.db.models.constraints import CheckConstraint
from django.db.models import Q
from django.dispatch import receiver
from django.core.validators import MinLengthValidator


class ComponenteCurricular(models.Model):
    codigo = models.CharField(primary_key=True, max_length=7, validators=[MinLengthValidator(7)])
    nome = models.CharField(max_length=80)
    num_semestre = models.IntegerField()
    carga_horaria = models.IntegerField()
    departamento = models.CharField(max_length=80)
    obrigatorio = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Componente Curricular'
        verbose_name_plural = 'Componentes Curriculares'

        constraints = [
            CheckConstraint(check=Q(num_semestre__gte="0"), name="semestre_maior_igual_0"),
            CheckConstraint(check=Q(num_semestre__lte="6"), name="semestre_menor_igual_6"),
            CheckConstraint(check=Q(carga_horaria__gte="0"), name="carga_horaria_maior_0")
        ]

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nome.upper())


class Turma(models.Model):
    cod_componente = models.ForeignKey(ComponenteCurricular, related_name='turma_disciplina', on_delete=models.CASCADE)
    num_turma = models.PositiveSmallIntegerField()
    horario = models.CharField(max_length=15)
    professor = models.ManyToManyField("Professor", related_name='turma_professor', null=True, blank=True)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        constraints = [
            models.UniqueConstraint(fields=['cod_componente', 'num_turma'], name='unique_cod_componente_num_turma'),
        ]

    def __str__(self):
        return "{} - Turma {}".format(self.cod_componente, self.num_turma)


class Professor(models.Model):
    nome_prof = models.CharField(max_length=80)
    horas_semanais = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    #turmas = models.ManyToManyField("Turma", related_name='professor_turma', null=True, blank=True)

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return self.nome_prof


@receiver(post_save, sender=Professor)
def corrige_horas(sender, instance, created, **kwargs):
    if created:
        instance.horas_semanais = 0
        instance.save()


#@receiver(m2m_changed, sender=Professor.turmas.through)
#def calcular_horas_alteracao(sender, instance, action, **kwargs):
    #if action in ['post_add', 'post_remove', 'post_clear']:
        #horas = 0
        #for turmas in instance.turmas.all():
            #horas += turmas.cod_componente.carga_horaria / 15

        #instance.horas_semanais = horas
        #instance.save()


#@receiver(post_save, sender=Turma)
#def calcular_horas_criacao(sender, instance, created=True, **kwargs):
    #if created:
        #horas = 0
        #quant = instance.professor.all().count()

        #for profs in instance.professor.all():
            #horas = instance.cod_componente.carga_horaria / 15
            #profs.horas_semanais += horas/instance.professor.all().count()
            #profs.save()

#@receiver(m2m_changed, sender=Turma.professor.through)
#def calcular_horas_alteracao(sender, instance, action, reverse, model, pk_set, **kwargs):
    #if action in ['post_add', 'post_remove', 'post_clear']:
        #for id_profs in pk_set:
            #professor = Professor.objects.get(pk=id_profs)
            #professor.horas_semanais += (instance.cod_componente.carga_horaria / 15)
            #professor.save()

        #instance.save()