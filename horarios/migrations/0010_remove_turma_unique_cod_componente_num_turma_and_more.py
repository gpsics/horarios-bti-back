# Generated by Django 4.2.3 on 2023-10-02 12:12

from django.db import migrations, models
import horarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0009_turma_num_vagas'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='turma',
            name='unique_cod_componente_num_turma',
        ),
        migrations.AlterField(
            model_name='componentecurricular',
            name='carga_horaria',
            field=models.PositiveSmallIntegerField(validators=[horarios.models.validar_carga_horaria]),
        ),
        migrations.AlterField(
            model_name='componentecurricular',
            name='nome_comp',
            field=models.CharField(error_messages='O nome do componente deve ter no mínimo 1 caractere e no máximo 80.', max_length=80),
        ),
        migrations.AlterField(
            model_name='turma',
            name='horario',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='turma',
            name='num_vagas',
            field=models.PositiveSmallIntegerField(default=0, error_messages='O número de vagas deve no mínimo 0.'),
        ),
        migrations.AddConstraint(
            model_name='turma',
            constraint=models.UniqueConstraint(fields=('cod_componente', 'num_turma'), name='Já existe turma com esse número.'),
        ),
    ]