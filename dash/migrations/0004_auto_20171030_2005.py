# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 22:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0003_auto_20171030_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='palestrante',
            name='show_home',
            field=models.NullBooleanField(default=False, verbose_name='Mostrar na pagina inicial?'),
        ),
    ]