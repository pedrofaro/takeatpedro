# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-12-03 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onshop_auto', '0013_codigo_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codigo',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/codeqrs/'),
        ),
    ]
