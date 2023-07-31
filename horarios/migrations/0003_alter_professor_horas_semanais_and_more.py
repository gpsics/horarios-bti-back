# Generated by Django 4.2.3 on 2023-07-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0002_professor_turma_professor_turmas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='horas_semanais',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='turma',
            unique_together={('cod_componente', 'num_turma')},
        ),
    ]
