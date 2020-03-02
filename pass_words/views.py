# -*- coding: utf8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string

from .models import ControleNovaSenha
from .forms import NovaSenhaForm, RenovaSenhaForm

from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template


def reseta_senha(request):
    if request.method == 'POST':
        novasenha = form = NovaSenhaForm(request.POST)
    
        if form.is_valid():
            email = form.cleaned_data["email"]
            token = get_random_string(length=32)
            
            try:#Se já existe um token para criação de nova senha, atualiza em caso negativo cria uma nova.
                novasenha = get_object_or_404(ControleNovaSenha, email=email)
                novasenha.token = token
                novasenha.data_criacao=datetime.datetime.now()
                novasenha.save()
            except:
                novasenha = ControleNovaSenha.objects.create(email=email, token = token, data_criacao=timezone.now())
                
            #Contexto para o Email     
            c = {
                'token': token,
                'protocol': request.scheme,
                'domain': request.META['HTTP_HOST']
            }
            message = render_to_string('pass_words/password_reset_email.html', c)
            
            #Enviando mensagem para a pessoa que requisitou nova senha
            send_mail('[OnShop] Nova Senha', message, 'sistema@visaexpress.com.br', [email])

            return render(request, 'pass_words/password_reset_done.html')
    else:
    
        novasenha = NovaSenhaForm()

    return render(request, 'pass_words/password_reset_form.html', {'form': novasenha})
    
def reseta_confirma(request, token=None):
    novasenha = get_object_or_404(ControleNovaSenha, token=token)

    if request.method == 'POST':
        renovasenha = form = RenovaSenhaForm(request.POST)
    
        if form.is_valid():
                
            if novasenha.data_criacao >= timezone.now() - datetime.timedelta(days=1): #Garante somente 24 horas de validade do token
                password = form.cleaned_data["password1"]
                user = get_object_or_404(User, email=novasenha.email)
                user.set_password(password)
                user.save()
                
                novasenha.delete()#Garante que o token foi acessado somente uma única vez para a mudança de senha
    
            return render(request, 'pass_words/password_reset_complete.html')
    else:
        renovasenha = RenovaSenhaForm()
    
    return render(request, 'pass_words/password_reset_confirm.html', {'form': renovasenha})