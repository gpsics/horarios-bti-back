from django.db.models.signals import pre_delete, post_save, m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from decimal import Decimal

from horarios.models import Professor, Turma


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