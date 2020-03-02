# -*- coding: utf8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ControleNovaSenha(models.Model): #Classe para controle de Nova Senha
    email = models.EmailField()
    token = models.TextField(null=True, blank=True) #Gerado para controle de troca de senha
    data_criacao = models.DateTimeField(null=True,blank=True)#Data de foi criada a NovaSenha
    

    