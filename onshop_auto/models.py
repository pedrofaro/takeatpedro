# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile

from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import qrcode #https://github.com/lincolnloop/python-qrcode

# Create your models here.

#class LogoEstabelecimento(models.Model): 
'''
Na verdade será um acréscimo de informação dentro do OnSHop_Core para inserção da Logo para a página inicial do LogoEstabelecimento
'''

class CategoriaAuto(models.Model):
	'''
	Categoria dos Produtos. Ex: Entradas, Bebidas, Hamburguers, etc...
	'''
	nome = models.CharField(max_length=255)
	descricao = models.TextField(null=True, blank=True)
	tempo_preparo = models.CharField(max_length=255)

	def __unicode__(self):
		#return '%s' % (self.sem_acento)
		return self.nome

class AtributoAuto(models.Model):
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

class ProdutoAuto(models.Model):
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
	categoria = models.ForeignKey(CategoriaAuto,  on_delete=models.CASCADE)
	descricao = models.TextField(null=True, blank=True)
	preco = models.DecimalField(null=True, max_digits=8, decimal_places=2)
	preco_promocao = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Caso seja preenchido, substitui o preço normal
	atributos = models.ManyToManyField('AtributoAuto', blank=True)
	pedido_especial = models.TextField(null=True, blank=True)

	esgotado = models.IntegerField(choices=RESPOSTAS, default=RESPOSTA_NAO)

	def __unicode__(self):
		return self.nome

class PerguntaAuto(models.Model):
	RESPOSTA_EXCLUSIVA = 1
	RESPOSTA_MULTIPLA = 2
	RESPOSTA_RECORRENTE = 3
	RESPOSTAS = (
		(RESPOSTA_EXCLUSIVA, u'Resposta Exclusiva'),
		(RESPOSTA_MULTIPLA, u'Resposta Múltipla'),
		(RESPOSTA_RECORRENTE, u'Resposta Recorrente'),
	)
	produto = models.ForeignKey(ProdutoAuto, null=True, blank=True, on_delete=models.CASCADE)
	pergunta = models.CharField(max_length=800)
	tipo = models.IntegerField(choices=RESPOSTAS, default=RESPOSTA_EXCLUSIVA)
	limite = models.IntegerField(null=True, blank=True) #Se houver multipla ou recorrente quantas respostas podem ser dadas

	def __unicode__(self):
		return self.pergunta
		
	def get_respostas(self):
		respostas = RespostaAuto.objects.filter(pergunta=self)

		return respostas

class RespostaAuto(models.Model):
	pergunta = models.ForeignKey(PerguntaAuto, null=True, blank=True, on_delete=models.CASCADE)
	resposta = models.CharField(max_length=400)
	sem_acento = models.CharField(max_length=400, null=True, blank=True) #Para uso interno e possibilidade de aparecer acentuação no cliente final
	preco_adicional = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Caso a opção acrescente algo no valor

	def __unicode__(self):
		#return self.sem_acento
		return self.resposta

class ComplementoModeloAuto(models.Model):
	'''
	Lista de Perguntas e Respostas que podem servir de Modelo para os Produtos
	'''
	nome_modelo = models.CharField(max_length=800)


class PerguntaModeloAuto(models.Model):
	RESPOSTA_EXCLUSIVA = 1
	RESPOSTA_MULTIPLA = 2
	RESPOSTA_RECORRENTE = 3
	RESPOSTAS = (
		(RESPOSTA_EXCLUSIVA, u'Resposta Exclusiva'),
		(RESPOSTA_MULTIPLA, u'Resposta Múltipla'),
		(RESPOSTA_RECORRENTE, u'Resposta Recorrente'),
	)
	modelo = models.ForeignKey(ComplementoModeloAuto, null=True, blank=True, on_delete=models.CASCADE) #Fica linkado a uma lista de Complementos Modelo
	pergunta = models.CharField(max_length=800)
	tipo = models.IntegerField(choices=RESPOSTAS, default=RESPOSTA_EXCLUSIVA)
	limite = models.IntegerField(null=True, blank=True) #Se houver multipla ou recorrente quantas respostas podem ser dadas

	def __unicode__(self):
		return self.pergunta

class RespostaModeloAuto(models.Model):
	pergunta = models.ForeignKey(PerguntaModeloAuto, null=True, blank=True, on_delete=models.CASCADE)
	resposta = models.CharField(max_length=400)
	preco_adicional = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Caso a opção acrescente algo no valor

	def __unicode__(self):
		return self.resposta

'''
class QRMesa(models.Model):
    imagem = models.ImageField(
        null=True,
        blank=True,
        upload_to='codeqrs',
        )

    def __str__(self):
        return "%s" % self.id

    def download_image(self, url):
        output_file = StringIO()
        qr = qrcode.QRCode(
            border=2,
        )
        qr.add_data("TakeAt" + str(self.id))
        img = qr.make_image()
        img.save(output_file, "PNG")
        self.imagem.save(str(self.id) +".png", ContentFile(output_file.getvalue()), save=False)

    def criar_code(self, *args, **kwargs):
        
        #Esse objeto somente é chamado depois de criado o objeto
        
        self.download_image("TakeAt" + str(self.id))
        super(QRMesa, self).save(*args, **kwargs)
'''

class Codigo(models.Model):
	
	codigo = models.CharField(max_length=5)
	endereco = models.CharField(null=True, blank=True, max_length=300)
	scheme = models.CharField(null=True, blank=True, max_length=6)
	#qr_code = models.ForeignKey(QRMesa, unique=True, blank=True, null=True)

	qr_code = models.ImageField(
        null=True,
        blank=True,
        upload_to='uploads/codeqrs/',
        )

	def download_image(self, url):
		output_file = StringIO()
		qr = qrcode.QRCode(
			border=2,
		)
		#qr.add_data("TakeAt" + str(self.codigo))
		qr.add_data(str(self.scheme) +'://' + str(self.endereco) + '/auto/codigo/' + 
str(self.codigo))
		img = qr.make_image()
		img.save(output_file, "PNG")
		self.qr_code.save(str(self.id) +".png", ContentFile(output_file.getvalue()), save=False)

	def criar_code(self, *args, **kwargs):
		'''
		Esse objeto somente é chamado depois de criado o objeto
		'''
		self.download_image(self.codigo)
		super(Codigo, self).save(*args, **kwargs)


class Mesa(models.Model):
	MESA_FECHADA = 1
	MESA_ABERTA = 2
	STATUS_MESA = (
		(MESA_FECHADA, u'Mesa Fechada'),
		(MESA_ABERTA, u'Mesa Aberta'),
	)
	numero_mesa = models.CharField(max_length=3)
	codigo_mesa = models.ForeignKey(Codigo, null=True, blank=True, on_delete=models.CASCADE)
	status = models.IntegerField(choices=STATUS_MESA, default=MESA_FECHADA)

	def get_comanda_total(self):
		comanda = None
		try:
			comanda = get_object_or_404(Comanda, mesa=self, status=Comanda.COMANDA_ABERTA)
		except:
			pass

		if comanda:
			return comanda.total
		else:
			return 0.00

	def get_comanda_id(self):
		comanda = None
		try:
			comanda = get_object_or_404(Comanda, mesa=self, status=Comanda.COMANDA_ABERTA)
		except:
			pass

		if comanda:
			return comanda.id
		else:
			return None

	def __unicode__(self):
		return self.numero_mesa

# ------------------------------------------
# ------------------- Classes referentes ao Pedido -----------------------
class Comanda(models.Model):
	COMANDA_ABERTA = 1 
	COMANDA_FECHADA = 2
	STATUS_COMANDA = (
		(COMANDA_ABERTA, 'Comanda Aberta'), 
		(COMANDA_FECHADA, 'Comanda Fechada'),
	)
	
	status = models.IntegerField(choices=STATUS_COMANDA, default=COMANDA_ABERTA)
	mesa = models.ForeignKey(Mesa, null=True, blank=True, on_delete=models.CASCADE)
	
	hora_abertura = models.DateTimeField(null=True, blank=True)
	hora_fechamento = models.DateTimeField(null=True, blank=True)

	total = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

class ComandaSession(models.Model):
	'''
	Classe que consegue identificar que usuários estão em qual comanda
	'''
	session_key = models.CharField(max_length=50)#request.session.session_key
	comanda = models.ForeignKey(Comanda, null=True, blank=True, on_delete=models.CASCADE)

class ProdutoPedidoAuto(models.Model):
	produto = models.ForeignKey(ProdutoAuto, null=True, blank=True, on_delete=models.CASCADE)
	complemento = models.TextField(null=True, blank=True)
	quantidade = models.IntegerField(null=True, blank=True)
	preco_produto = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Para facilitar na impressão pois, o preço pode variar depois de comprado
	adicional = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
	total = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

	def __unicode__(self):
		return self.produto.nome

class CompradorPedidoAuto(models.Model):
	session_key = models.CharField(max_length=50)#request.session.session_key - Através da Session Key é possível localizar a pessoa que está fazendo o pedido
	nome = models.CharField(max_length=400, null=True, blank=True)
	sobrenome = models.CharField(max_length=400, null=True, blank=True)
	telefone = models.CharField(max_length=400)
	email = models.CharField(max_length=400, null=True, blank=True)

# ------------------------------------------
# ------------------- Garçom -----------------------

class Garcom(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.CharField(max_length=20)
    senha = models.CharField(max_length=20)
    token = models.CharField(max_length=20, null=True, blank=True)#Para garantir segurança de que é o próprio Garçom acessando 

    hora_criacao = models.DateTimeField(null=True, blank=True, auto_now_add=True)

# ------------------------------------------
# ------------------------------------------

class PedidoAuto(models.Model):
	PEDIDO_CARRINHO = 1 #Ainda está sendo realizado ou foi abandonado
	PEDIDO_NOVO = 2
	PEDIDO_ANDAMENTO = 3
	PEDIDO_FINALIZADO = 4
	PEDIDO_REJEITADO = 5	
	STATUS_PEDIDO = (
		(PEDIDO_CARRINHO, 'Pedido no Carrinho'), 
		(PEDIDO_NOVO, 'Novo Pedido'),
		(PEDIDO_ANDAMENTO, 'Em Andamento'),
		(PEDIDO_FINALIZADO, 'Pedido Entregue'),
		(PEDIDO_REJEITADO, 'Pedido Rejeitado'),
	)
	'''
	PAGAMENTO_DINHEIRO = 1
	PAGAMENTO_CARTAO = 2
	PAGAMENTO = (
		('PAGAMENTO_DINHEIRO', 'Pagamento em Dinheiro'),
		('PAGAMENTO_CARTAO', 'Pagamento em Cartão'),
	)
	'''
	comanda = models.ForeignKey(Comanda, blank=True, null=True, on_delete=models.CASCADE)
	garcom = models.ForeignKey(Garcom, blank=True, null=True, on_delete=models.CASCADE) #Adicionado a Chave para Garçom

	produtos = models.ManyToManyField('ProdutoPedidoAuto', blank=True)
	quantidade_itens = models.IntegerField(default=0, null=True,blank=True) #Para poder atualizar a barra footer do cliente
	total = models.DecimalField(default=0,null=True, blank=True, max_digits=8, decimal_places=2)

	comprador = models.ForeignKey(CompradorPedidoAuto, blank=True, null=True, on_delete=models.CASCADE)
	session_key = models.CharField(max_length=50, blank=True, null=True)#Pela session_key é possível identificar o pedido feito por algum dispositivo enquanto ainda não é registrado pelo formulário

	pedido_especial = models.TextField(null=True, blank=True)
	hora_criacao = models.DateTimeField(null=True, blank=True)
	hora_atendimento = models.DateTimeField(null=True, blank=True)

	status = models.IntegerField(choices=STATUS_PEDIDO, default=PEDIDO_CARRINHO)

class ItemPedidoAuto(models.Model):
	'''
	Necessário para poder fazer mudanças de itens para outras mesas ou cancelar o item
	Objeto criado no momento em que o Pedido é enviado para o estabelecimento
	'''
	comanda = models.ForeignKey(Comanda, blank=True, null=True, on_delete=models.CASCADE)
	pedido_atrelado = models.ForeignKey(PedidoAuto, blank=True, null=True, on_delete=models.CASCADE)
	comprador = models.ForeignKey(CompradorPedidoAuto, blank=True, null=True, on_delete=models.CASCADE)

	hora_criacao = models.DateTimeField(null=True, blank=True)
	hora_atendimento = models.DateTimeField(null=True, blank=True)

	produto = models.ForeignKey(ProdutoAuto, null=True, blank=True, on_delete=models.CASCADE)
	complemento = models.TextField(null=True, blank=True)
	quantidade = models.IntegerField(null=True, blank=True)
	preco_produto = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2) #Para facilitar na impressão pois, o preço pode variar depois de comprado
	adicional = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)
	total = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=2)

	def __unicode__(self):
		return self.produto.nome


class MensagemAuto(models.Model):
	MENSAGEM_NAO_ATENDIDA = 1 
	MENSAGEM_ATENDIDA = 2
	STATUS_MENSAGEM = (
		(MENSAGEM_NAO_ATENDIDA, 'Mensagem Nao Atendida'), 
		(MENSAGEM_ATENDIDA, 'Mensagem Atendida'),
	)

	comanda = models.ForeignKey(Comanda, blank=True, null=True, on_delete=models.CASCADE)
	mensagem = models.TextField()
	hora_criacao = models.DateTimeField(null=True, blank=True)

	status = models.IntegerField(choices=STATUS_MENSAGEM, default=MENSAGEM_NAO_ATENDIDA)

class QAvaliado(models.Model):
	'''
	Modelo que apresenta o que está sendo avaliado pelo Lojista
	'''
	nome_primeiro_campo = models.CharField(max_length=50, default='Tempo')
	nome_segundo_campo = models.CharField(max_length=50, default='Limpeza')
	nome_terceiro_campo = models.CharField(max_length=50, default='Atendimento')
	nome_quarto_campo = models.CharField(max_length=50, default='Produtos')


class Avaliacao(models.Model):
	nota_primeiro_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
	nota_segundo_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
	nota_terceiro_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
	nota_quarto_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)

	mensagem = models.TextField(blank=True, null=True)
	hora_criacao = models.DateTimeField(null=True, blank=True)

class NotaMedia(models.Model):
	qtde_dias = models.IntegerField(null=True, blank=True) #Para saber se em 1, 7 ou 30 dias

	nota_primeiro_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
	nota_segundo_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
	nota_terceiro_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
	nota_quarto_campo = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)

	hora_calculada = models.DateTimeField(null=True, blank=True) #Para ver se é necessário fazer novo cálculo