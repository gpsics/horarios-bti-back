# Generated by Django 4.2.3 on 2023-08-23 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horarios', '0003_alter_componentecurricular_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentecurricular',
            name='departamento',
            field=models.CharField(choices=[('DETEC', 'Departamento de Engenharias e Tecnologia'), ('DCSAH', 'Departamento de Ciências Sociais Aplicadas e Humanas'), ('DECEN', 'Departamento de Ciências Exatas e Naturais')], max_length=80),
        ),
    ]
