# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2020-01-23 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onshop_auto', '0017_codigo_scheme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codigo',
            name='endereco',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='codigo',
            name='scheme',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
