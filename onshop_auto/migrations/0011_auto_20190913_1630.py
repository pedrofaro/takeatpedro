# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-09-13 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onshop_auto', '0010_mensagemauto'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensagemauto',
            name='hora_criacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mensagemauto',
            name='status',
            field=models.IntegerField(choices=[(1, 'Mensagem Nao Atendida'), (2, 'Mensagem Atendida')], default=1),
        ),
    ]