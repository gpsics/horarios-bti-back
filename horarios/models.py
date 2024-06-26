from django.db import models
from django.db.models.constraints import CheckConstraint
from django.db.models import Q
from django.core.validators import MinLengthValidator


# Modelo de Componente Curricular com seus devidos atributos
class ComponenteCurricular(models.Model):
    DEPARTAMENTO = (
        ("DETEC", "Departamento de Engenharias e Tecnologia"),
        ("DCSAH", "Departamento de Ciências Sociais Aplicadas e Humanas"),
        ("DECEN", "Departamento de Ciências Exatas e Naturais")
    )

    codigo = models.CharField(primary_key=True, max_length=7, validators=[MinLengthValidator(7)])
    nome_comp = models.CharField(max_length=80)
    num_semestre = models.IntegerField(blank=True, default=0)
    carga_horaria = models.PositiveSmallIntegerField()
    departamento = models.CharField(max_length=80, choices=DEPARTAMENTO)
    obrigatorio = models.BooleanField(default=False)

    class Meta:
        # Nome que será representado esse modelo
        verbose_name = 'Componente Curricular'
        verbose_name_plural = 'Componentes Curriculares'

        # Algumas das restrições do modelo Componente Curricular
        constraints = [
            CheckConstraint(check=Q(num_semestre__gte="0"), name="semestre_maior_igual_0"),
            CheckConstraint(check=Q(num_semestre__lte="6"), name="semestre_menor_igual_6"),
            CheckConstraint(check=Q(carga_horaria__gte="0"), name="carga_horaria_maior_0"),
            CheckConstraint(check=~Q(obrigatorio=True, num_semestre="0"),
                            name="semestre_diferente_zero_componente_obrigatorio"),
        ]

    def save(self, *args, **kwargs):
        self.nome_comp = self.nome_comp.upper()
        super(ComponenteCurricular, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nome_comp)


# Modelo de Turma Curricular com seus devidos atributos e relacionamentos
class Turma(models.Model):
    cod_componente = models.ForeignKey(ComponenteCurricular, related_name='turma_disciplina', on_delete=models.CASCADE)
    num_turma = models.PositiveSmallIntegerField()
    horario = models.CharField(max_length=80)
    num_vagas = models.PositiveSmallIntegerField(default=0)
    professor = models.ManyToManyField("Professor", related_name='turma_professor', null=True, blank=True)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

        # Restrição de especificando que a junção cod_componente e num_turma são atributos únicos
        constraints = [
            models.UniqueConstraint(fields=['cod_componente', 'num_turma'], name='Já existe turma com esse número.'),
        ]

    def save(self, *args, **kwargs):
        self.horario = self.horario.upper()
        super(Turma, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - Turma {}".format(self.cod_componente, self.num_turma)


# Modelo de Professor com seus devidos atributos
class Professor(models.Model):
    nome_prof = models.CharField(max_length=80, unique=True)
    horas_semanais = models.DecimalField(max_digits=2, decimal_places=0, default=0)

    class Meta:
        # Nome que será representado esse modelo
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def save(self, *args, **kwargs):
        self.nome_prof = self.nome_prof.upper()
        super(Professor, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome_prof
