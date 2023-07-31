# Generated by Django 4.2.3 on 2023-07-28 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_prof', models.CharField(max_length=80)),
                ('horas_semanais', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_turma', models.IntegerField()),
                ('horario', models.CharField(max_length=15)),
                ('cod_componente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turma_disciplina', to='horarios.componentecurricular')),
                ('professor', models.ManyToManyField(blank=True, null=True, related_name='turma_professor', to='horarios.professor')),
            ],
        ),
        migrations.AddField(
            model_name='professor',
            name='turmas',
            field=models.ManyToManyField(blank=True, null=True, related_name='professor_turma', to='horarios.turma'),
        ),
    ]
