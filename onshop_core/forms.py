# -*- coding: utf-8 -*-
try:
    import Image
except ImportError:
    from PIL import Image

from django import forms

from .models import Categoria, Atributo, Produto, Estabelecimento, Pergunta, Resposta, ComplementoModelo, PerguntaModelo, RespostaModelo, CompradorPedido, LocalRetiradaPedido, BairrosAtendidos, PushSignal, PMesa, PProduto, PPedidos, PPedidosFormaPag, PFormasPag

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class PMesaModelForm(forms.ModelForm):
    class Meta:
        model = PMesa
        fields = ['id_restaurante', 'id_mesa']

class PProdutoModelForm(forms.ModelForm):
    class Meta:
        model = PProduto
        fields = ['id_restaurante', 'id_prod', 'nome', 'preco']

class PFormasPagModelForm(forms.ModelForm):
    class Meta:
        model = PFormasPag
        fields = ['id_restaurante', 'id_forma', 'forma']

class PPedidosFormaPagModelForm(forms.ModelForm):
    class Meta:
        model = PPedidosFormaPag
        fields = ['forma', 'id_pedido', 'valor' , 'mesa']


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        exclude = ('cat_slug',)

    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['descricao'].widget.attrs.update({'class' : 'form-control'})

class AtributoForm(forms.ModelForm):

    class Meta:
        model = Atributo
        exclude = ('icone',)

    def __init__(self, *args, **kwargs):
        super(AtributoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        '''
        self.fields['icone'].widget.attrs.update({'class' : 'form-control'})
        self.fields['icone'].required = True
        '''

class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto
        exclude = ('pedido_especial','thumbnail',)

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['esgotado'].widget.attrs.update({'class' : 'form-control'})
        self.fields['nome'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['descricao'].widget.attrs.update({'class' : 'form-control'})
        self.fields['imagem'].widget.attrs.update({'class' : 'form-control'})
        self.fields['categoria'].widget.attrs.update({'class' : 'form-control'})
        self.fields['preco'].widget.attrs.update({'class' : 'form-control'})
        self.fields['preco_promocao'].widget.attrs.update({'class' : 'form-control'})
        self.fields['atributos'].widget.attrs.update({'class' : 'form-control'})


    def save(self, *args, **kwargs):
        """Metodo declarado para criar miniatura da imagem depois de salvar"""
        foto = super(ProdutoForm, self).save(*args, **kwargs)

        if 'imagem' in self.changed_data:
            extensao = foto.imagem.name.split('.')[-1]
            foto.imagem.name = slugify(foto.imagem.name)
            foto.save()

            foto.thumbnail = 'uploads/produtos/%d.%s'%(foto.id, extensao)

            miniatura = auxiliar = Image.open(foto.imagem.path)

            width, height = miniatura.size

            LARGURA = 75 #Largura da Imagem a ser apresentada no template
            ALTURA = 75 #Altura da Imagem a ser apresentada no template

            if LARGURA > width or ALTURA > height: #Garante que a imagem inserida é maior que o que vai ser apresentado
                raise forms.ValidationError(u"Imagem precisa ser maior.")

            auxiliar.thumbnail((10000, ALTURA), Image.ANTIALIAS) #Traz a imagem para a altura do que será apresentado
            auxiliar.save(foto.thumbnail.path, quality=100) # Tem que salvar e retornar pois o thumbnail retorna None
            auxiliar = Image.open(foto.thumbnail.path)

            w , h = auxiliar.size

            if w >= LARGURA: #Então está correta a altura e corta só as barras laterais
                x1 = (w-LARGURA)/2
                x2 = (w+LARGURA)/2
                auxiliar = auxiliar.crop((x1, 0, x2, ALTURA))
                auxiliar.save(foto.thumbnail.path, quality=100)
            else: #Então tem que se pegar pela largura e cortar faixas superiores e inferiores
                auxiliar2 = Image.open(foto.imagem.path) #Para não dar problemas com o auxiliar na imagem
                auxiliar2.thumbnail((LARGURA, 10000), Image.ANTIALIAS)
                auxiliar2.save(foto.thumbnail.path)
                auxiliar2 = Image.open(foto.thumbnail.path)
                w , h = auxiliar2.size
                y1 = (h-ALTURA)/2
                y2 = (h+ALTURA)/2
                auxiliar2 = auxiliar2.crop((0, y1, LARGURA, y2))
                auxiliar2.save(foto.thumbnail.path, quality=100)
                
        return foto

class EstabelecimentoForm(forms.ModelForm):

    class Meta:
        model = Estabelecimento
        exclude = ('status',)

    def __init__(self, *args, **kwargs):
        super(EstabelecimentoForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['endereco'].widget.attrs.update({'class' : 'form-control'})
        self.fields['telefone'].widget.attrs.update({'class' : 'form-control'})
        self.fields['observacao'].widget.attrs.update({'class' : 'form-control'})
        self.fields['horario_abertura'].widget.attrs.update({'class' : 'time ui-timepicker-input form-control'})
        self.fields['horario_fechamento'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tempo_espera'].widget.attrs.update({'class' : 'form-control'})
        self.fields['pedido_minimo'].widget.attrs.update({'class' : 'form-control', 'placeholder': '0.00'})

class PerfilForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password1'].required = False
        self.fields['password2'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password2'].required = False


    def clean(self):
        cleaned_data = super(PerfilForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("As senhas são diferentes!")

        return cleaned_data


class PerguntaForm(forms.ModelForm):

    class Meta:
        model = Pergunta
        exclude = ('produto',)

    def __init__(self, *args, **kwargs):
        super(PerguntaForm, self).__init__(*args, **kwargs)
        self.fields['pergunta'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['tipo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['limite'].widget.attrs.update({'class' : 'form-control'})

class RespostaForm(forms.ModelForm):

    class Meta:
        model = Resposta
        exclude = ('pergunta',)

    def __init__(self, *args, **kwargs):
        super(RespostaForm, self).__init__(*args, **kwargs)
        self.fields['resposta'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['preco_adicional'].widget.attrs.update({'class' : 'form-control'})

class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple): #Fazendo com que a informação de preço adicional apareça para o cliente final
    option_template_name = 'onshop_core/detail_options.html'

class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj

class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.resposta

class ProdutoMobileForm(forms.Form):

    def __init__(self, questions, *args, **kwargs):
        super(ProdutoMobileForm, self).__init__(*args, **kwargs)
        for i, question in enumerate(questions):
            if question.limite: #Se possui limitação de quantidade de escolhas
                self.max_choices = question.limite
            else:
                self.max_choices = 3 #Deixar como padrão para nao dar erro
            if question.tipo == Pergunta.RESPOSTA_EXCLUSIVA:
                self.fields['question_%d' % i] = MyModelChoiceField(
                    queryset=Resposta.objects.filter(pergunta=question),
                    label=question,
                    label_suffix='?',
                    widget=forms.RadioSelect(attrs={'tipo':'exclusiva'}),
                    empty_label=None,
                    required=True
                )
            if question.tipo == Pergunta.RESPOSTA_MULTIPLA:
                self.fields['question_%d' % i] = MyModelMultipleChoiceField(
                    queryset=Resposta.objects.filter(pergunta=question),
                    label=question,
                    label_suffix='?',
                    widget=MyCheckboxSelectMultiple,
                    required=False
                )
            if question.tipo == Pergunta.RESPOSTA_RECORRENTE:
                #self.fields['question_%d' % i] = forms.TextInput()
                self.fields['question_%d' % i] = forms.ModelChoiceField(
                    queryset=Resposta.objects.filter(pergunta=question),
                    label=question,
                    label_suffix='?',
                    widget=forms.TextInput(attrs={'recorrente': 'True' })
                    )
                #self.fields['question_%d' % i].widget.attrs['tipo'] = 'teste'

                respostas = Resposta.objects.filter(pergunta=question)
                for resposta in respostas:
                    self.fields['%d' % resposta.id] = forms.ModelChoiceField(
                        queryset=None,
                        label=resposta.resposta,
                        required=False,
                        initial=0,
                        widget=forms.NumberInput(attrs={
                            'js-group':'id_%d' % i,
                            'recorrente': 'True',
                            'resposta':'True',
                            'clique': 0,
                            'min':0,
                            'max':self.max_choices,
                            'step':1
                            })
                    )

    def clean(self, value):
        if value and self.max_choices and len(value) > self.max_choices:
            raise forms.ValidationError('São aceitos até %s escolhas.' % (apnumber(self.max_choices)))


class ComplementoModeloForm(forms.ModelForm):

    class Meta:
        model = ComplementoModelo
        exclude = ('',)


    def __init__(self, *args, **kwargs):
        super(ComplementoModeloForm, self).__init__(*args, **kwargs)
        self.fields['nome_modelo'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização


class PerguntaModeloForm(forms.ModelForm):

    class Meta:
        model = PerguntaModelo
        exclude = ('modelo',)

    def __init__(self, *args, **kwargs):
        super(PerguntaModeloForm, self).__init__(*args, **kwargs)
        self.fields['pergunta'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['tipo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['limite'].widget.attrs.update({'class' : 'form-control'})

class RespostaModeloForm(forms.ModelForm):

    class Meta:
        model = RespostaModelo
        exclude = ('pergunta',)

    def __init__(self, *args, **kwargs):
        super(RespostaModeloForm, self).__init__(*args, **kwargs)
        self.fields['resposta'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
        self.fields['preco_adicional'].widget.attrs.update({'class' : 'form-control'})


class AtribuirForm(forms.Form):
    produtos = forms.MultipleChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(AtribuirForm, self).__init__(*args, **kwargs)
        self.fields['produtos'] = forms.MultipleChoiceField(
            choices=[[x.id, x.nome] for x in Produto.objects.all()],
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )

class ContatoForm(forms.ModelForm):
    class Meta:
        model = CompradorPedido
        exclude = ('',)


class LocalRetiradaPedidoForm(forms.ModelForm):
    class Meta:
        model = LocalRetiradaPedido
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(LocalRetiradaPedidoForm, self).__init__(*args, **kwargs)
        self.fields['endereco'].widget.attrs.update({'id' : 'searchTextField', 'autocomplete': 'off' }) #Necessário para o Maps
        self.fields['numero'].widget.attrs.update({'placeholder': 'Digite um Numero'})
        self.fields['numero'].required = True
        self.fields['ed_apto_bloco'].widget.attrs.update({ 'placeholder': 'Digite Edificio, Apto ou Bloco'})
        self.fields['pto_referencia'].widget.attrs.update({ 'placeholder': 'Digite um Ponto de Referencia'})

class BairroForm(forms.ModelForm):
    class Meta:
        model = BairrosAtendidos
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(BairroForm, self).__init__(*args, **kwargs)
        self.fields['bairro'].widget.attrs.update({'class' : 'form-control'})


class AcessarForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"))
    password = forms.CharField(widget=forms.PasswordInput, label=_("Senha"))

    def __init__(self, *args, **kwargs):
        super(AcessarForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'name':'email',
            'type': 'email',
            'class': 'form-control input-lg',
            'placeholder': 'E-mail'
        })
        self.fields['password'].widget.attrs.update({
            'type': 'password',
            'class': 'form-control input-lg',
            'placeholder': 'Senha',
            'id':'password'
        })

    def clean(self):
        cleaned_data = super(AcessarForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = None

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass            

            if user is not None:
                if user.check_password(password):
                    return cleaned_data
                else:
                    raise forms.ValidationError(_("Senha incorreta."))
            else:
                raise forms.ValidationError("E-mail não registrado. Por favor faça seu cadastro no link Participar.")#_("E-mail not registered.")

        return cleaned_data

    def acessar(self):
        '''
        Como os dados já foram validados não há problema em buscar o usuário sem preocupação
        '''
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass            

        return user

class PushSignalForm(forms.ModelForm):
    class Meta:
        model = PushSignal
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(PushSignalForm, self).__init__(*args, **kwargs)
        self.fields['app_id'].widget.attrs.update({'class' : 'form-control'})
        self.fields['authorization'].widget.attrs.update({'class' : 'form-control'})

#class FotoPerfilForm(forms.ModelForm):
#    class Meta:
#        model = FotoPerfil
#        exclude = ('',)
        
#    def save(self, *args, **kwargs):
        """Metodo declarado para criar miniatura da imagem depois de salvar"""
'''        imagem = super(FotoPerfilForm, self).save(*args, **kwargs)
        
        if 'foto_perfil_original' in self.changed_data:
            extensao = imagem.foto_perfil_original.name.split('.')[-1]
            imagem.save()

            imagem.foto_perfil_thumbnail = 'uploads/perfil/%d.%s'%(imagem.id, extensao)

            miniatura = auxiliar = Image.open(imagem.foto_perfil_original.path)
            
            width, height = miniatura.size
            
            LARGURA = 200 #Largura da Imagem a ser apresentada no template
            ALTURA = 200 #Altura da Imagem a ser apresentada no template
            
            if LARGURA > width or ALTURA > height: #Garante que a imagem inserida é maior que o que vai ser apresentado
                raise forms.ValidationError(u"Imagem precisa ser maior.")
            
            auxiliar.thumbnail((10000, ALTURA), Image.ANTIALIAS) #Traz a imagem para a altura do que será apresentado
            auxiliar.save(imagem.foto_perfil_thumbnail.path) # Tem que salvar e retornar pois o thumbnail retorna None
            auxiliar = Image.open(imagem.foto_perfil_thumbnail.path)
            w , h = auxiliar.size
            
            if w >= LARGURA: #Então está correta a altura e corta só as barras laterais
                x1 = (w-LARGURA)/2
                x2 = (w+LARGURA)/2
                auxiliar = auxiliar.crop((x1, 0, x2, ALTURA))
                auxiliar.save(imagem.foto_perfil_thumbnail.path)
            else: #Então tem que se pegar pela largura e cortar faixas superiores e inferiores
                auxiliar2 = Image.open(imagem.foto_perfil_original.path) #Para não dar problemas com o auxiliar na imagem
                auxiliar2.thumbnail((LARGURA, 10000), Image.ANTIALIAS)
                auxiliar2.save(imagem.foto_perfil_thumbnail.path)
                auxiliar2 = Image.open(imagem.foto_perfil_thumbnail.path)
                w , h = auxiliar2.size
                y1 = (h-ALTURA)/2
                y2 = (h+ALTURA)/2
                auxiliar2 = auxiliar2.crop((0, y1, LARGURA, y2))
                auxiliar2.save(imagem.foto_perfil_thumbnail.path)
                
        return imagem'''