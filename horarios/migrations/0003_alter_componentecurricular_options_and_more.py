# Generated by Django 4.2.3 on 2023-08-18 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0002_alter_componentecurricular_codigo_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='componentecurricular',
            options={'verbose_name': 'Componente Curricular', 'verbose_name_plural': 'Componentes Curriculares'},
        ),
        migrations.AlterModelOptions(
            name='professor',
            options={'verbose_name': 'Professor', 'verbose_name_plural': 'Professores'},
        ),
        migrations.AlterModelOptions(
            name='turma',
            options={'verbose_name': 'Turma', 'verbose_name_plural': 'Turmas'},
        ),
        migrations.RemoveField(
            model_name='professor',
            name='turmas',
        ),
    ]
