# -*- coding: utf8 -*- 
from django.conf.urls import url

from . import views

app_name = 'pass_words'
urlpatterns = [

    url(r'^reset/$', views.reseta_senha, name='reseta_senha'),
    url(r'^resetconfirm/(?P<token>[-\w]+)/$', views.reseta_confirma, name='reseta_confirma'),
    #url(r'^resetcomplete/$', views.reset_complete, {'template_name': 'visa_registration/password_reset_complete.html'}, name='password_reset_complete'),    
]