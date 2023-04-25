# Generated by Django 4.1.2 on 2022-10-29 08:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_advuser_first_name_alter_advuser_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='first_name',
            field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='invalid_first_name', message='Имя введено не правильно', regex='[а-яА-ЯёЁ]')], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='last_name',
            field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='invalid_last_name', message='Фамилия введена не правильно', regex='[а-яА-ЯёЁ]')], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='middle_name',
            field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(code='invalid_middle_name', message='Отвество введено не правильно', regex='[а-яА-ЯёЁ]')], verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='username',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_username', message='Имя пользователя введено не правильно', regex='^[a-z]*$')], verbose_name='Имя пользователя'),
        ),
    ]
