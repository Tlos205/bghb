# Generated by Django 5.0.11 on 2025-02-02 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Полное название страны')),
                ('short_name', models.CharField(max_length=255, verbose_name='Краткое название страны')),
                ('code_3', models.CharField(max_length=3, verbose_name='Код страны из 3 букв')),
                ('code_2', models.CharField(max_length=2, verbose_name='Код страны из 2 букв')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='EntryRegime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regime', models.CharField(max_length=255, verbose_name='Режим въезда в РФ')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Примечание')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='countries.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Режим въезда',
                'verbose_name_plural': 'Режимы въезда',
            },
        ),
    ]
