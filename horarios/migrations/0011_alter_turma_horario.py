# Generated by Django 4.2.3 on 2023-10-10 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0010_remove_turma_unique_cod_componente_num_turma_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turma',
            name='horario',
            field=models.CharField(max_length=80),
        ),
    ]