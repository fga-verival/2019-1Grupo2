# Generated by Django 2.2 on 2019-06-08 14:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TransactionalFunctions', '0002_auto_20190608_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionalfunction',
            name='name',
            field=models.CharField(max_length=250, validators=[django.core.validators.MinLengthValidator(4, message='O nome deve ter pelo menos 3 caracteres')], verbose_name='Nome'),
        ),
    ]