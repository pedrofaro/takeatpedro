# -*- coding: utf-8 -*-
"""onshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('onshop_auto.tela_principal_urls')), #Fazer uma página principal de recebimento de pedidos
    url(r'^on/', include('onshop_core.urls')),
    url(r'^senha/', include('pass_words.urls')), #Rotinas de Esqueceu a Senha
    url(r'^auto/', include('onshop_auto.urls')), #Funções do Autoatendimento
    url(r'^OneSignalSDKWorker.js', TemplateView.as_view(template_name='onshop_core/OneSignalSDKWorker.js', content_type='application/javascript')),
    url(r'^OneSignalSDKUpdaterWorker.js', TemplateView.as_view(template_name='onshop_core/OneSignalSDKUpdaterWorker.js', content_type='application/javascript')),
]
