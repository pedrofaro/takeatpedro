# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from . import views

app_name = 'onshop_auto_tela_principal'

urlpatterns = [
	url(r'^$', views.tela_principal, name='tela_principal'), #Tela Inicial do aplicativo
]

