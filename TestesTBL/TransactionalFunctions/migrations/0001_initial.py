# Generated by Django 2.2 on 2019-06-05 12:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionalFunction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Nome')),
                ('functionality_type', models.IntegerField(choices=[(1, 'EE'), (2, 'CE'), (3, 'SE')], verbose_name='Tipo de Funcionalidade')),
                ('ALR_aumount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Parâmetro 1 (ALR)')),
                ('DER_aumount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Parâmetro 2 (DER)')),
                ('counter_name', models.CharField(max_length=250, verbose_name='Nome do Contador')),
                ('date', models.DateField(auto_now=True, verbose_name='Data')),
            ],
            options={
                'verbose_name': 'Função Transacional',
                'verbose_name_plural': 'Funções Transacional',
            },
        ),
    ]
