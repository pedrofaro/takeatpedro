# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-11-27 00:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onshop_auto', '0012_itempedidoauto'),
    ]

    operations = [
        migrations.AddField(
            model_name='codigo',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='codeqrs'),
        ),
    ]
