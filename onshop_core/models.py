# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from decimal import Decimal

# Create your models here.

class PMesa(models.Model):
	id_restaurante = models.IntegerField()
	id_mesa = models.IntegerField()


class PProduto(models.Model):
	id_restaurante = models.IntegerField('Id do Restaurante')
	id_prod = models.IntegerField('Id do Produto')
	nome = models.CharField(max_length=200)
	preco = models.DecimalField(decimal_places=2, max_digits=4)

	def __str__(self):
		return self.nome

class PPedidos(models.Model):
	id_pedido = models.IntegerField('Id do Restaurante')
	id_restaurante = models.IntegerField('Id do Restaurante')
	id_mesa = models.IntegerField('Número da Mesa')
	id_produto = models.IntegerField('Id do Produto')
	preco = models.DecimalField(decimal_places=2, max_digits=4)

	def __str__(self):
		return self.id_pedido

class PFormasPag(models.Model):
	id_forma = models.IntegerField('Id da forma de pagamento')
	id_restaurante = models.IntegerField('Id do Restaurante')
	forma = models.CharField('Forma de pagamento', max_length=200)

	def __str__(self):
		return self.forma

class PPedidosFormaPag(models.Model):
	id_pedido = models.IntegerField('Id do Pedido')
	mesa = models.IntegerField('Mesa', default=0)
	valor = models.DecimalField(decimal_places=2, max_digits=4)
	forma = models.CharField('Forma de pagamento', max_length=200)



class Estabelecimento(models.Model):
	ABERTO = 1
	FECHADO = 2
	STATUS_ESTABELECIMENTO = (
		(ABERTO, 'Aberto'),
		(FECHADO, 'Fechado'),
	)
	nome = models.CharField(max_length=255)
	endereco = models.TextField()
	telefone = models.CharField(max_length=25,null=True, blank=True)
	observacao = models.CharField(max_length=100,null=True, blank=True) #Para informação de bandeiras de cartão aceitas e etc...
	horario_abertura = models.TimeField(null=True, blank=True)
	horario_fechamento = models.TimeField(null=True, blank=True)
	status = models.IntegerField(choices=STATUS_ESTABELECIMENTO, default=FECHADO)
	tempo_espera = models.CharField(default='50 minutos',max_length=25,null=True, blank=True)
	pedido_minimo = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2)

	def __str__(self):
		return self.nome

class BairrosAtendidos(models.Model):
	estabelecimento = models.ForeignKey(Estabelecimento, null=True, blank=True, on_delete=models.CASCADE)
	bairro = models.CharField(max_length=255)

	def __unicode__(self):
		return self.bairro

##class Perfil(models.Model)
##	user = models.OnetoOneField(User)


class Categoria(models.Model):
	'''
	Categoria dos Produtos. Ex: Entradas, Bebidas, Hamburguers, etc...
	'''
	nome = models.CharField(max_length=255)
	descricao = models.TextField(null=True, blank=True)

	def __unicode__(self):
		#return '%s' % (self.sem_acento)
		return self.nome

class Atributo(models.Model):
	'''
	Atributo de um Produto. Ex: Vegano, Picante, Especial, etc...
	'''
	nome = models.CharField(max_length=255)
	icone = models.ImageField(
		null=True,
		upload_to='uploads/icones/',
		verbose_name='Atributo'
		)

	def __str__(self):
		return self.nome

class Produto(models.Model):
	RESPOSTA_NAO = 0
	RESPOSTA_SIM = 1
	RESPOSTAS = (
		(RESPOSTA_NAO, 'Nao'),
		(RESPOSTA_SIM, 'Sim'),
	)

	imagem = models.ImageField(
		null=True,
		blank=True,
		upload_to='uploads/produtos/',
		verbose_name='ImagemProduto'
		)
	thumbnail = models.ImageField(
		null=True,
		blank=True,
		upload_to='uploads/produtos/',
		verbose_name='ThumbnailProduto'
		)
	nome = models.CharField(max_length=255)
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	descricao = models.TextField(null=True, blank=True)
	preco = models.DecimalField(null=True, max_digits=8, decimal_places=2)
	preco_promocao = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Caso seja preenchido, substitui o preço normal
	atributos = models.ManyToManyField('Atributo', blank=True)
	pedido_especial = models.TextField(null=True, blank=True)

	esgotado = models.IntegerField(choices=RESPOSTAS, default=RESPOSTA_NAO)

	def __unicode__(self):
		return self.nome

class Pergunta(models.Model):
	RESPOSTA_EXCLUSIVA = 1
	RESPOSTA_MULTIPLA = 2
	RESPOSTA_RECORRENTE = 3
	RESPOSTAS = (
		(RESPOSTA_EXCLUSIVA, u'Resposta Exclusiva'),
		(RESPOSTA_MULTIPLA, u'Resposta Múltipla'),
		(RESPOSTA_RECORRENTE, u'Resposta Recorrente'),
	)
	produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.CASCADE)
	pergunta = models.CharField(max_length=800)
	tipo = models.IntegerField(choices=RESPOSTAS, default=RESPOSTA_EXCLUSIVA)
	limite = models.IntegerField(null=True, blank=True) #Se houver multipla ou recorrente quantas respostas podem ser dadas

	def __unicode__(self):
		return self.pergunta
		
	def get_respostas(self):
		respostas = Resposta.objects.filter(pergunta=self)

		return respostas

class Resposta(models.Model):
	pergunta = models.ForeignKey(Pergunta, null=True, blank=True, on_delete=models.CASCADE)
	resposta = models.CharField(max_length=400)
	sem_acento = models.CharField(max_length=400, null=True, blank=True) #Para uso interno e possibilidade de aparecer acentuação no cliente final
	preco_adicional = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Caso a opção acrescente algo no valor

	def __unicode__(self):
		#return self.sem_acento
		return self.resposta

class ComplementoModelo(models.Model):
	'''
	Lista de Perguntas e Respostas que podem servir de Modelo para os Produtos
	'''
	nome_modelo = models.CharField(max_length=800)


class PerguntaModelo(models.Model):
	RESPOSTA_EXCLUSIVA = 1
	RESPOSTA_MULTIPLA = 2
	RESPOSTA_RECORRENTE = 3
	RESPOSTAS = (
		(RESPOSTA_EXCLUSIVA, u'Resposta Exclusiva'),
		(RESPOSTA_MULTIPLA, u'Resposta Múltipla'),
		(RESPOSTA_RECORRENTE, u'Resposta Recorrente'),
	)
	modelo = models.ForeignKey(ComplementoModelo, null=True, blank=True, on_delete=models.CASCADE) #Fica linkado a uma lista de Complementos Modelo
	pergunta = models.CharField(max_length=800)
	tipo = models.IntegerField(choices=RESPOSTAS, default=RESPOSTA_EXCLUSIVA)
	limite = models.IntegerField(null=True, blank=True) #Se houver multipla ou recorrente quantas respostas podem ser dadas

	def __unicode__(self):
		return self.pergunta

class RespostaModelo(models.Model):
	pergunta = models.ForeignKey(PerguntaModelo, null=True, blank=True, on_delete=models.CASCADE)
	resposta = models.CharField(max_length=400)
	preco_adicional = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Caso a opção acrescente algo no valor

	def __unicode__(self):
		return self.resposta

#SIGNALS
from django.db.models import signals 
from django.template.defaultfilters import slugify
from unicodedata import normalize

def remover_acentos(txt):
	return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')

def categoria_pre_save(signal, instance, sender, **kwargs):
	sem_acento = remover_acentos(instance.nome)
	instance.sem_acento = sem_acento

#signals.pre_save.connect(categoria_pre_save, sender=Categoria)

def produto_pre_save(signal, instance, sender, **kwargs):
	sem_acento = remover_acentos(instance.nome)
	instance.sem_acento = sem_acento

#signals.pre_save.connect(produto_pre_save, sender=Produto)

def resposta_pre_save(signal, instance, sender, **kwargs):
	sem_acento = remover_acentos(instance.resposta)
	instance.sem_acento = sem_acento

#signals.pre_save.connect(resposta_pre_save, sender=Resposta)

# ------------------------------------------
# ------------------- Classe referente ao Relatório -----------------------
class Relatorio(models.Model):
	dia = models.DateTimeField()
	quantidade_pedidos = models.IntegerField(null=True, blank=True, default=0)
	total = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

# ------------------------------------------
# ------------------- Classes referentes ao Pedido -----------------------

class ProdutoPedido(models.Model):
	produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.CASCADE)
	complemento = models.TextField(null=True, blank=True)
	quantidade = models.IntegerField(null=True, blank=True)
	preco_produto = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Para facilitar na impressão pois, o preço pode variar depois de comprado
	adicional = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
	total = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

	def __unicode__(self):
		return self.produto.nome

class LocalRetiradaPedido(models.Model):
	endereco = models.CharField(max_length=400)
	numero = models.CharField(max_length=255, null=True, blank=True)
	ed_apto_bloco = models.CharField(max_length=400, null=True, blank=True)
	pto_referencia = models.CharField(max_length=400, null=True, blank=True)

class CompradorPedido(models.Model):
	nome = models.CharField(max_length=400)
	sobrenome = models.CharField(max_length=400, null=True, blank=True)
	telefone = models.CharField(max_length=400)
	email = models.CharField(max_length=400)

class OpcaoPagamento(models.Model):
	forma = models.CharField(max_length=400, null=True, blank=True)
	troco = models.CharField(max_length=400, null=True, blank=True)

class Pedido(models.Model):
	PEDIDO_CARRINHO = 1 #Ainda está sendo realizado ou foi abandonado
	PEDIDO_NOVO = 2
	PEDIDO_ANDAMENTO = 3
	PEDIDO_FINALIZADO = 4
	STATUS_PEDIDO = (
		(PEDIDO_CARRINHO, 'Pedido no Carrinho'), 
		(PEDIDO_NOVO, 'Novo Pedido'),
		(PEDIDO_ANDAMENTO, 'Em Andamento'),
		(PEDIDO_FINALIZADO, 'Pedido Finalizado'),
	)
	'''
	PAGAMENTO_DINHEIRO = 1
	PAGAMENTO_CARTAO = 2
	PAGAMENTO = (
		('PAGAMENTO_DINHEIRO', 'Pagamento em Dinheiro'),
		('PAGAMENTO_CARTAO', 'Pagamento em Cartão'),
	)
	'''
	session_key = models.CharField(max_length=50)#request.session.session_key
	produtos = models.ManyToManyField('ProdutoPedido', blank=True)
	quantidade_itens = models.IntegerField(default=0, null=True,blank=True) #Para poder atualizar a barra footer do cliente
	total = models.DecimalField(default=0,null=True, blank=True, max_digits=8, decimal_places=2)

	retirada = models.ForeignKey(LocalRetiradaPedido, blank=True, null=True, on_delete=models.CASCADE)
	comprador = models.ForeignKey(CompradorPedido, blank=True, null=True, on_delete=models.CASCADE)
	opcao_pagamento = models.ForeignKey(OpcaoPagamento, blank=True, null=True, on_delete=models.CASCADE)

	pedido_especial = models.TextField(null=True, blank=True)
	hora_criacao = models.DateTimeField(null=True, blank=True)
	hora_atendimento = models.DateTimeField(null=True, blank=True)

	status = models.IntegerField(choices=STATUS_PEDIDO, default=PEDIDO_CARRINHO)


class PushSignal(models.Model):
	app_id = models.CharField(max_length=200, null=True, blank=True)
	authorization = models.CharField(max_length=200, null=True, blank=True)
