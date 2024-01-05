# Generated by Django 4.2.3 on 2024-01-05 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0011_alter_turma_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentecurricular',
            name='carga_horaria',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='componentecurricular',
            name='nome_comp',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='turma',
            name='num_vagas',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
