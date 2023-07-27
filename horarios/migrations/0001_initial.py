# Generated by Django 4.2.3 on 2023-07-27 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ComponenteCurricular',
            fields=[
                ('codigo', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=80)),
                ('num_semestre', models.IntegerField()),
                ('carga_horaria', models.IntegerField(default=0)),
                ('departamento', models.CharField(blank=True, max_length=80, null=True)),
                ('obrigatorio', models.BooleanField(default=False)),
            ],
        ),
    ]
