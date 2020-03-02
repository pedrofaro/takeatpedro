# -*- coding: utf8 -*-
from django import forms

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import ControleNovaSenha

class NovaSenhaForm(forms.Form):#Recebe o email e verifica se é cadastrado
    email = forms.EmailField(label=_("E-mail"))
    
    def __init__(self, *args, **kwargs):
        super(NovaSenhaForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'name':'email',
            'type': 'email',
            'class': 'form-control input-lg',
            'placeholder': 'E-mail'
        })
    
    def clean(self):
        cleaned_data = super(NovaSenhaForm, self).clean()
        email = cleaned_data.get('email')
    
        if email:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("E-mail não registrado. Por favor entre em contato com a Visa Express.")#_("E-mail not registered.")

        return cleaned_data
        

class RenovaSenhaForm(forms.Form):#Recebe senha e confere se são iguais
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super(RenovaSenhaForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'name':'senha',
            'type': 'senha',
            'class': 'form-control input-lg',
            'placeholder': 'Senha'
        })
        self.fields['password2'].widget.attrs.update({
            'name':'senha2',
            'type': 'senha2',
            'class': 'form-control input-lg',
            'placeholder': 'Confirme a Senha'
        })
        
    def clean(self):
        cleaned_data = super(RenovaSenhaForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError("As senhas são diferentes!")
            
        return cleaned_data