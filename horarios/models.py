from django.db import models
from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.db.models.constraints import CheckConstraint
from django.db.models import Q
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
import re


# Função responsável por validar e verificar o formato/quantidade de horários
def validar_horario(horarios, carga_horaria):
    vetor_horarios = horarios.split()
    contador_h = 0

    # Verifica se o horário está dentro do limite para a carga horária do componente
    if not len(vetor_horarios) == carga_horaria / 15:
        raise ValidationError(f'Horário "{horarios}" inválido')

    for index in range(len(vetor_horarios)):
        # Verifica se o horário está seguindo a sua expressão regular ou seu modelo
        if not re.match(r'^[2-7]+[MmTtNn][1-6]+$', vetor_horarios[index]):
            raise ValidationError(f'Formato inválido do horário "{vetor_horarios[index]}"')

        # Ordena de forma crescente as partes contendo número na expressão
        dias_ordenado = "".join(sorted(re.sub(r'[MmNnTt].*', '', vetor_horarios[index])))
        horas_ordenado = "".join(sorted(re.sub(r'^.*[MmNnTt]', '', vetor_horarios[index])))

        # Verifica se nas partes contendo números, contém apenas números
        if re.search(r'[a-zA-Z]', dias_ordenado) or re.search(r'[a-zA-Z]', horas_ordenado):
            raise ValidationError(f'Formato inválido do horário "{vetor_horarios[index]}"')

        # Incrementa a quantidade de horas no horario no contador_h
        contador_h += len(dias_ordenado) * len(horas_ordenado)

        turno = (re.search(r'[MmNnTt]', vetor_horarios[index])).group().upper()

        # Após as informações serem ordenadas e verificadas, são postas na string novamente
        vetor_horarios[index] = dias_ordenado + turno + horas_ordenado

    # Verifica se a quantidade de horas presente no horário está correto
    if not contador_h == carga_horaria / 15:
        raise ValidationError(f'Quantidade de horas inválida no horário "{contador_h} - {carga_horaria}".')

    return " ".join(vetor_horarios)


# Função que verifica e validar se o valor da carga horária está correta
def validar_carga_horaria(value):
    if not value > 0 or not value % 15 == 0:
        raise ValidationError(f'Carga horária ({value}) deve maior que 0 e divisível por 15.')


# Modelo de Componente Curricular com seus devidos atributos
class ComponenteCurricular(models.Model):
    DEPARTAMENTO = (
        ("DETEC", "Departamento de Engenharias e Tecnologia"),
        ("DCSAH", "Departamento de Ciências Sociais Aplicadas e Humanas"),
        ("DECEN", "Departamento de Ciências Exatas e Naturais")
    )

    codigo = models.CharField(primary_key=True, max_length=7, validators=[MinLengthValidator(7)])
    nome_comp = models.CharField(max_length=80, error_messages="O nome do componente deve ter no mínimo 1 caractere e "
                                                               "no máximo 80.")
    num_semestre = models.IntegerField(blank=True, default=0)
    carga_horaria = models.PositiveSmallIntegerField(validators=[validar_carga_horaria])
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
                            name="semestre_diferente_zero_componente_obrigatorio")
        ]

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper()
        self.nome_comp = self.nome_comp.upper()
        super(ComponenteCurricular, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nome_comp)


# Modelo de Turma Curricular com seus devidos atributos e relacionamentos
class Turma(models.Model):
    cod_componente = models.ForeignKey(ComponenteCurricular, related_name='turma_disciplina', on_delete=models.CASCADE)
    num_turma = models.PositiveSmallIntegerField()
    horario = models.CharField(max_length=80)
    num_vagas = models.PositiveSmallIntegerField(default=0, error_messages="O número de vagas deve no mínimo 0.")
    professor = models.ManyToManyField("Professor", related_name='turma_professor', null=True, blank=True)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'

        # Restrição de especificando que a junção cod_componente e num_turma são atributos únicos
        constraints = [
            models.UniqueConstraint(fields=['cod_componente', 'num_turma'], name='Já existe turma com esse número.'),
        ]

    def save(self, *args, **kwargs):
        self.horario = validar_horario(self.horario, self.cod_componente.carga_horaria)
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


# Signal que monitora a criação de um objeto de Professor
@receiver(post_save, sender=Professor)
def corrige_horas(sender, instance, created, **kwargs):
    # Sempre que um Professor é criado, o campo horas_semanais é atribuído o valor 0
    if created:
        instance.horas_semanais = 0
        instance.save()


# Signal que monitora a exclusão de um objeto de Turma
@receiver(pre_delete, sender=Turma)
def delete_turma(sender, instance, **kwargs):
    horas = (instance.cod_componente.carga_horaria / 15)

    # Sempre que uma Turma é deletada, os professores presente na Turma tem suas horas decrementadas
    for profs in instance.professor.all():
        profs.horas_semanais -= Decimal(horas)
        profs.save()


# Signal que monitora o relacionamente ManyToMany de Turma e Professor
@receiver(m2m_changed, sender=Turma.professor.through)
def ajuste_horas_professor(sender, instance, model, action, pk_set, **kwargs):
    horas = (instance.cod_componente.carga_horaria / 15)

    # Sempre antes de uma instância do relacionando ser salva, os professores presente nela tem suas horas incrementada
    if action == "pre_add":
        for id_prof in pk_set:
            profs = Professor.objects.get(pk=id_prof)

            # Caso o professor tenham atingido 20 horas semanais, a ação retorna um erro, senão incrementa as horas
            if (profs.horas_semanais + Decimal(horas)) > 20:
                raise ValidationError(f'Quantidade de horas semanais máxima do professor "{profs}" atinginda.')
            else:
                profs.horas_semanais += Decimal(horas)
                profs.save()

    # Sempre que um ou mais professores são removidos da relação com turma, os removidos tem suas horas decrementada
    elif action == "post_remove":
        # Itera a cerca dos id dos professores removidos da relação
        for id_prof in pk_set:
            profs = Professor.objects.get(pk=id_prof)

            profs.horas_semanais -= Decimal(horas)
            profs.save()

m2m_changed.connect(ajuste_horas_professor, sender=Turma.professor.through)