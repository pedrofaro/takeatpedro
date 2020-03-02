# -*- coding: utf-8 -*-
try:
    import Image
except ImportError:
    from PIL import Image

from django import forms

from .models import CategoriaAuto, AtributoAuto, ProdutoAuto, PerguntaAuto, RespostaAuto, ComplementoModeloAuto, PerguntaModeloAuto, RespostaModeloAuto, Mesa, Codigo, CompradorPedidoAuto, MensagemAuto, QAvaliado, Avaliacao, Garcom

from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

class CategoriaForm(forms.ModelForm):

	class Meta:
		model = CategoriaAuto
		exclude = ('cat_slug',)

	def __init__(self, *args, **kwargs):
		super(CategoriaForm, self).__init__(*args, **kwargs)
		self.fields['nome'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['descricao'].widget.attrs.update({'class' : 'form-control'})
		self.fields['tempo_preparo'].widget.attrs.update({'class' : 'form-control'})

class AtributoForm(forms.ModelForm):

	class Meta:
		model = AtributoAuto
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
		model = ProdutoAuto
		exclude = ('pedido_especial','thumbnail',)

	def __init__(self, *args, **kwargs):
		super(ProdutoForm, self).__init__(*args, **kwargs)
		self.fields['esgotado'].widget.attrs.update({'class' : 'form-control'})
		self.fields['nome'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['descricao'].widget.attrs.update({'class' : 'form-control'})
		self.fields['imagem'].widget.attrs.update({'class' : 'form-control'})
		#self.fields['imagem'].required = False
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

			foto.thumbnail = 'uploads/auto_prod/%d.%s'%(foto.id, extensao)

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

class PerguntaForm(forms.ModelForm):

	class Meta:
		model = PerguntaAuto
		exclude = ('produto',)

	def __init__(self, *args, **kwargs):
		super(PerguntaForm, self).__init__(*args, **kwargs)
		self.fields['pergunta'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['tipo'].widget.attrs.update({'class' : 'form-control'})
		self.fields['limite'].widget.attrs.update({'class' : 'form-control'})

class RespostaForm(forms.ModelForm):

	class Meta:
		model = RespostaAuto
		exclude = ('pergunta',)

	def __init__(self, *args, **kwargs):
		super(RespostaForm, self).__init__(*args, **kwargs)
		self.fields['resposta'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['preco_adicional'].widget.attrs.update({'class' : 'form-control'})

class ComplementoModeloForm(forms.ModelForm):

	class Meta:
		model = ComplementoModeloAuto
		exclude = ('',)


	def __init__(self, *args, **kwargs):
		super(ComplementoModeloForm, self).__init__(*args, **kwargs)
		self.fields['nome_modelo'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização


class PerguntaModeloForm(forms.ModelForm):

	class Meta:
		model = PerguntaModeloAuto
		exclude = ('modelo',)

	def __init__(self, *args, **kwargs):
		super(PerguntaModeloForm, self).__init__(*args, **kwargs)
		self.fields['pergunta'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['tipo'].widget.attrs.update({'class' : 'form-control'})
		self.fields['limite'].widget.attrs.update({'class' : 'form-control'})

class RespostaModeloForm(forms.ModelForm):

	class Meta:
		model = RespostaModeloAuto
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
			choices=[[x.id, x.nome] for x in ProdutoAuto.objects.all()],
			required=False,
			widget=forms.CheckboxSelectMultiple()
		)

class MesaForm(forms.ModelForm):

	class Meta:
		model = Mesa
		exclude = ('codigo_mesa','status',)

	def __init__(self, *args, **kwargs):
		super(MesaForm, self).__init__(*args, **kwargs)
		self.fields['numero_mesa'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização

class MesasForm(forms.Form):
	numero_mesa = forms.ChoiceField()

	def __init__(self, *args, **kwargs):
		mesa_id = kwargs.pop('id_mesa')
		super(MesasForm, self).__init__(*args, **kwargs)
		self.fields['numero_mesa'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['numero_mesa'] = forms.ChoiceField(choices=[(choice.id, choice.numero_mesa) for choice in Mesa.objects.all().exclude(id=mesa_id).order_by('numero_mesa')])

def get_mesas_abertas(id_mesa):
	mesas = Mesa.objects.filter(status=Mesa.MESA_ABERTA).exclude(id=id_mesa).order_by('numero_mesa')
	choices_list = []
	for choice in mesas:
		choices_list.append((choice.id, choice.numero_mesa))
	return choices_list

class MesaAbertaForm(forms.Form):
	numero_mesa = forms.ChoiceField()

	def __init__(self, *args, **kwargs):
		mesa_id = kwargs.pop('id_mesa')
		super(MesaAbertaForm, self).__init__(*args, **kwargs)
		self.fields['numero_mesa'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['numero_mesa'] = forms.ChoiceField(choices=get_mesas_abertas(mesa_id))

class CodigoForm(forms.ModelForm):

	class Meta:
		model = Codigo
		exclude = ('',)

	def __init__(self, *args, **kwargs):
		super(CodigoForm, self).__init__(*args, **kwargs)
		self.fields['codigo'].widget.attrs.update({'class' : 'form-control', 'placeholder': u'Digitar Código'})


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
			if question.tipo == PerguntaAuto.RESPOSTA_EXCLUSIVA:
				self.fields['question_%d' % i] = MyModelChoiceField(
					queryset=RespostaAuto.objects.filter(pergunta=question),
					label=question,
					label_suffix='?',
					widget=forms.RadioSelect(attrs={'tipo':'exclusiva'}),
					empty_label=None, 
					required=True
				)
			if question.tipo == PerguntaAuto.RESPOSTA_MULTIPLA:
				self.fields['question_%d' % i] = MyModelMultipleChoiceField(
					queryset=RespostaAuto.objects.filter(pergunta=question),
					label=question,
					label_suffix='?',
					widget=MyCheckboxSelectMultiple,
					required=False
				)
			if question.tipo == PerguntaAuto.RESPOSTA_RECORRENTE:
				#self.fields['question_%d' % i] = forms.TextInput()
				self.fields['question_%d' % i] = forms.ModelChoiceField(
					queryset=RespostaAuto.objects.filter(pergunta=question),
					label=question,
					label_suffix='?',
					widget=forms.TextInput(attrs={'recorrente': 'True' })
					)
				#self.fields['question_%d' % i].widget.attrs['tipo'] = 'teste'

				respostas = RespostaAuto.objects.filter(pergunta=question)
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


class ContatoForm(forms.ModelForm):
	class Meta:
		model = CompradorPedidoAuto
		exclude = ('nome', 'email','sobrenome','session_key',)

def __init__(self, *args, **kwargs):
		super(ContatoForm, self).__init__(*args, **kwargs)
		self.fields['telefone'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		
class MensagemAutoForm(forms.ModelForm):
	class Meta:
		model = MensagemAuto
		exclude = ('comanda','hora_criacao','status',)
	'''
	def __init__(self, *args, **kwargs):
		super(MensagemAutoForm, self).__init__(*args, **kwargs)
		self.fields['mensagem'].widget.attrs['placeholder'] = 'Ex: Falta muito para o meu pedido ficar pronto?'
	'''

class AvaliacaoForm(forms.ModelForm):
	class Meta:
		model = QAvaliado
		exclude = ('',)

	def __init__(self, *args, **kwargs):
		super(AvaliacaoForm, self).__init__(*args, **kwargs)
		self.fields['nome_primeiro_campo'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['nome_segundo_campo'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['nome_terceiro_campo'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização
		self.fields['nome_quarto_campo'].widget.attrs.update({'class' : 'form-control'})#Necessário para a estilização

class NotaAvaliacaoForm(forms.ModelForm):
	class Meta:
		model = Avaliacao
		exclude = ('hora_criacao',)

	def __init__(self, *args, **kwargs):
		super(NotaAvaliacaoForm, self).__init__(*args, **kwargs)
		q_avaliado = QAvaliado.objects.all()[0]
		self.fields['nota_primeiro_campo'].label = q_avaliado.nome_primeiro_campo
		self.fields['nota_segundo_campo'].label = q_avaliado.nome_segundo_campo
		self.fields['nota_terceiro_campo'].label = q_avaliado.nome_terceiro_campo
		self.fields['nota_quarto_campo'].label = q_avaliado.nome_quarto_campo


class GarcomForm(forms.ModelForm):
	class Meta:
		model = Garcom
		exclude = ('token',)

	def __init__(self, *args, **kwargs):
		super(GarcomForm, self).__init__(*args, **kwargs)
		self.fields['nome'].widget.attrs.update({'class': 'form-control'})
		self.fields['usuario'].widget.attrs.update({'class': 'form-control'})
		self.fields['senha'].widget.attrs.update({'class': 'form-control'})


class AtendimentoForm(forms.ModelForm):
	senha = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = Garcom
		exclude = ('nome', 'hora_criacao',)

	def __init__(self, *args, **kwargs):
		super(AtendimentoForm, self).__init__(*args, **kwargs)
		self.fields['usuario'].widget.attrs.update({'class': 'form-control'})
		self.fields['senha'].widget.attrs.update({'class': 'form-control'})