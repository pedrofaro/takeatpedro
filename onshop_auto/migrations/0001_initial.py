# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-08-14 14:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AtributoAuto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('icone', models.ImageField(null=True, upload_to='uploads/icones/', verbose_name='Atributo')),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaAuto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoAuto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='uploads/produtos/', verbose_name='ImagemProduto')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/produtos/', verbose_name='ThumbnailProduto')),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('preco_promocao', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('pedido_especial', models.TextField(blank=True, null=True)),
                ('esgotado', models.IntegerField(choices=[(0, 'Nao'), (1, 'Sim')], default=0)),
                ('atributos', models.ManyToManyField(blank=True, to='onshop_auto.AtributoAuto')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onshop_auto.CategoriaAuto')),
            ],
        ),
    ]
