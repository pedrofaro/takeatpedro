# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from datetime import datetime, date, timedelta
from time import mktime
import pytz  # Apenas para poder usar o timezone
from django.http import JsonResponse
from decimal import Decimal
from django.db.models import Q
from cryptography.fernet import Fernet  # pip install cryptography

from .models import CategoriaAuto, AtributoAuto, ProdutoAuto, PerguntaAuto, RespostaAuto, ComplementoModeloAuto, \
    PerguntaModeloAuto, RespostaModeloAuto, Mesa, Codigo, Comanda, ComandaSession, PedidoAuto, ProdutoPedidoAuto, \
    CompradorPedidoAuto, MensagemAuto, ItemPedidoAuto, QAvaliado, Avaliacao, Garcom
from .forms import CategoriaForm, ProdutoForm, PerguntaForm, RespostaForm, ComplementoModeloForm, PerguntaModeloForm, \
    RespostaModeloForm, AtribuirForm, AtributoForm, MesaForm, CodigoForm, ProdutoMobileForm, ContatoForm, \
    MensagemAutoForm, MesaAbertaForm, MesasForm, AvaliacaoForm, NotaAvaliacaoForm, GarcomForm, AtendimentoForm

from onshop_core.models import Estabelecimento, PushSignal


# Create your views here.
# ------------ Tela Principal -----------
# ------------ -------------------
def tela_principal(request):
    try:
        estabelecimento = Estabelecimento.objects.all()[0]
    except:
        estabelecimento = Estabelecimento.objects.create(nome='Takeat')

    return render(request, 'onshop_auto/tela_principal.html', {'estabelecimento': estabelecimento})


# ------------ Produtos -----------
# ------------ -------------------
@login_required
def painel_produtos_auto(request):
    produtos = ProdutoAuto.objects.all()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_entregues = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_entregues.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/painel_produtos_auto.html',
                  {'produtos': produtos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def editar_produtos_auto(request, id=None):
    if id:
        auxiliar = get_object_or_404(ProdutoAuto, id=id)

    if request.method == 'POST':
        if id:
            produto = produto_form = ProdutoForm(request.POST, request.FILES, instance=auxiliar)
        else:
            produto = produto_form = ProdutoForm(request.POST, request.FILES)

        if produto_form.is_valid():
            produto = produto_form.save(commit=False)
            produto.save()
            produto_form.save_m2m()  # Necessario por conta do Many to Many e do commit False
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:admin_autoatendimento')

    else:
        if id:
            produto_form = ProdutoForm(instance=auxiliar)
        else:
            produto_form = ProdutoForm()

    return render(request, 'onshop_auto/form_produto.html', {'form': produto_form})


@login_required
def deletar_produto_auto(request, id):
    produto = get_object_or_404(ProdutoAuto, id=id)

    produto.delete()
    # TODO: Enviar Mensagem

    return redirect('onshop_auto:admin_autoatendimento')


# ------------ Categorias -----------
# ------------ -------------------
@login_required
def ver_categorias(request):
    categorias = CategoriaAuto.objects.all()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_entregues = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_entregues.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/categorias_auto.html',
                  {'categorias': categorias, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def editar_categorias(request, id=None):
    if id:
        auxiliar = get_object_or_404(CategoriaAuto, id=id)

    if request.method == 'POST':
        if id:
            categoria = categoria_form = CategoriaForm(request.POST, instance=auxiliar)
        else:
            categoria = categoria_form = CategoriaForm(request.POST)

        if categoria_form.is_valid():
            categoria.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_categorias_auto')
    else:
        if id:
            categoria_form = CategoriaForm(instance=auxiliar)
        else:
            categoria_form = CategoriaForm()

    return render(request, 'onshop_auto/form.html', {'form': categoria_form})


@login_required
def deletar_categoria(request, id):
    categoria = get_object_or_404(CategoriaAuto, id=id)

    categoria.delete()
    # TODO: Enviar Mensagem

    return redirect('onshop_auto:ver_categorias_auto')


# ------------ Atributos -----------
# ------------ -------------------
@login_required
def ver_atributos(request):
    atributos = AtributoAuto.objects.all()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_entregues = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_entregues.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/atributos.html',
                  {'atributos': atributos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def editar_atributos(request, id=None):
    if id:
        auxiliar = get_object_or_404(AtributoAuto, id=id)

    if request.method == 'POST':
        if id:
            atributo = atributo_form = AtributoForm(request.POST, request.FILES, instance=auxiliar)
        else:
            atributo = atributo_form = AtributoForm(request.POST, request.FILES)

        if atributo_form.is_valid():
            atributo = atributo_form.save(commit=False)
            atributo.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_atributos_auto')
    else:
        if id:
            atributo_form = AtributoForm(instance=auxiliar)
        else:
            atributo_form = AtributoForm()

    return render(request, 'onshop_auto/form_atributo.html', {'form': atributo_form})


@login_required
def deletar_atributos(request, id):
    atributo = get_object_or_404(AtributoAuto, id=id)

    atributo.delete()
    # TODO: Enviar Mensagem

    return redirect('onshop_auto:ver_atributos_auto')


# ------------ Administração das Mesas -----------
# ------------ -------------------
@login_required
def ver_mesas(request):
    mesas = Mesa.objects.all().order_by('numero_mesa')

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/mesas.html',
                  {'mesas': mesas, 'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def ver_mesas_abertas(request):
    mesas = Mesa.objects.filter(status=Mesa.MESA_ABERTA).order_by('numero_mesa')

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/mesas_abertas.html',
                  {'mesas': mesas, 'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def ver_detalhes_mesa_aberta(request, id_mesa):
    mesa = get_object_or_404(Mesa, id=id_mesa)
    comanda = get_object_or_404(Comanda, mesa=mesa, status=Comanda.COMANDA_ABERTA)
    itens_pedidos = ItemPedidoAuto.objects.filter(comanda=comanda)

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/mesa_aberta_detalhes.html',
                  {'mesa': mesa, 'pedidos': itens_pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def ver_ultimas_mesas_fechadas(request):
    '''
	Apresenta as últimas mesas fechadas de acordo com a Comanda
	'''
    comandas = Comanda.objects.filter(status=Comanda.COMANDA_FECHADA).order_by('-hora_fechamento')

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/mesas_fechadas.html',
                  {'comandas': comandas, 'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def editar_mesa(request, id=None):
    if id:
        auxiliar = get_object_or_404(Mesa, id=id)

    if request.method == 'POST':
        if id:
            mesa = mesa_form = MesaForm(request.POST, request.FILES, instance=auxiliar)
        else:
            mesa = mesa_form = MesaForm(request.POST, request.FILES)

        if mesa_form.is_valid():
            mesa = mesa_form.save(commit=False)
            mesa.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_mesas')
    else:
        if id:
            mesa_form = MesaForm(instance=auxiliar)
        else:
            mesa_form = MesaForm()

    return render(request, 'onshop_auto/form_mesa.html', {'form': mesa_form})


from random import randint


@login_required
def renovar_codigo_mesa(request, id=id):
    mesa = get_object_or_404(Mesa, id=id)
    novo_codigo = randint(0, 99999)

    if mesa.codigo_mesa == None:
        codigo = Codigo.objects.create(codigo=novo_codigo, endereco=request.META['HTTP_HOST'], scheme=request.scheme)
    else:
        codigo = mesa.codigo_mesa
        codigo.endereco = request.META['HTTP_HOST']
        codigo.scheme = request.scheme

    codigo.codigo = novo_codigo
    codigo.save()
    codigo.criar_code()  # Gera o novo qr code a partir do código renovado

    mesa.codigo_mesa = codigo
    mesa.save()

    return redirect('onshop_auto:ver_mesas')


@login_required
def deletar_mesa(request, id=id):
    mesa = get_object_or_404(Mesa, id=id)

    if mesa.codigo_mesa:
        mesa.codigo_mesa.delete()

    mesa.delete()

    return redirect('onshop_auto:ver_mesas')


# ------------ Fluxo de Pedidos (Usuário) -----------
# ------------ -------------------
def acessar_autoatendimento(request):
    '''
	Função que analisa se o celular já está cadastrado em alguma mesa.
	Caso positivo leva para o cardápio.
	Caso negativo leva para o registro do código da mesa.
	'''
    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA)
        return redirect('onshop_auto:ver_cardapio', id_comanda=comandasession.comanda.id)
    except:
        return redirect('onshop_auto:registrar_codigo')

    '''
		pass
	if comandasession:
		return redirect ('onshop_auto:ver_cardapio', comanda=comandasession.comanda.id)
	else:
		return redirect ('onshop_auto:registrar_codigo')
	'''


def registrar_codigo(request):
    if request.method == 'POST':
        codigo = codigo_form = CodigoForm(request.POST, request.FILES)

        if codigo_form.is_valid():
            codigo = codigo_form.cleaned_data['codigo']
            try:
                codigo = get_object_or_404(Codigo, codigo=codigo)
                mesa = get_object_or_404(Mesa, codigo_mesa=codigo)
            except:
                return redirect('onshop_auto:codigo_errado')

            if mesa.status == Mesa.MESA_FECHADA:  # Caso seja a primeira pessoa a abrir a mesa
                mesa.status = Mesa.MESA_ABERTA
                mesa.save()

            try:
                comanda = get_object_or_404(Comanda, mesa=mesa,
                                            status=Comanda.COMANDA_ABERTA)  # Tenta encontrar uma comanda em aberto da Mesa
            except:
                comanda = Comanda.objects.create(mesa=mesa, status=Comanda.COMANDA_ABERTA, hora_abertura=datetime.now(),
                                                 total=Decimal(0.0))  # Caso contrário abre uma comanda da Mesa

            try:
                comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                                   comanda=comanda)  # Caso já exista a ComandaSession não faz nada
            except:
                request.session.create()  # Cria uma nova sessão
                comandasession = ComandaSession.objects.create(session_key=request.session.session_key, comanda=comanda)

            return redirect('onshop_auto:ver_cardapio', id_comanda=comanda.id)

    else:
        codigo_form = CodigoForm()

    return render(request, 'onshop_auto/codigo_mesa_teste.html', {'form': codigo_form})


def codigo_errado(request):
    return render(request, 'onshop_auto/codigo_errado.html', {})


def ver_cardapio(request, id_comanda=None):  # O None é só para a função ser aceita quando é chamada por Ajax
    # Fazer controle se a comanda é a correta, caso negativo faz voltar para o registro da mesa
    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA, comanda__id=id_comanda)
    except:
        return redirect('onshop_auto:acessar_autoatendimento')

    categorias = CategoriaAuto.objects.all()
    lista = []
    for categoria in categorias:
        produtos = ProdutoAuto.objects.filter(categoria=categoria)
        lista.append([categoria, produtos])

    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
        quantidade = pedido.quantidade_itens
        total = pedido.total
    except:
        pedido = PedidoAuto.objects.create(comanda=comandasession.comanda, session_key=request.session.session_key,
                                           status=PedidoAuto.PEDIDO_CARRINHO)
        quantidade = 0
        total = 0.00

    try:
        estabelecimento = Estabelecimento.objects.all()[0]
    except:
        estabelecimento = Estabelecimento.objects.create(nome='OnShop')

    fuso_local = pytz.timezone('America/Sao_Paulo')
    hora_acesso = datetime.now(fuso_local).time()
    if estabelecimento.horario_abertura < estabelecimento.horario_fechamento:  # Significa que abre e fecha no mesmo dia
        if hora_acesso > estabelecimento.horario_abertura and hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    else:  # Significa que abre e fecha no dia seguinte
        if hora_acesso > estabelecimento.horario_abertura or hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO

    estabelecimento.save()

    mesa = comandasession.comanda.mesa.numero_mesa

    return render(request, 'onshop_auto/cardapio.html',
                  {'lista': lista, 'mesa': mesa, 'estabelecimento': estabelecimento, 'quantidade': quantidade,
                   'total': total, 'comanda': id_comanda, 'categorias': categorias, 'token': 0, 'id_garcom': 0})


def ver_carrinho(request):
    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA)
    except:
        pass
    # return redirect ('onshop_auto:acessar_autoatendimento')

    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
    except:
        pedido = None

    estabelecimento = Estabelecimento.objects.all()[0]

    return render(request, 'onshop_auto/carrinho.html', {'pedido': pedido, 'estabelecimento': estabelecimento})


def contato(request):
    '''
	Se já tem sessão é porque já fez algum pedido na mesa, caso negativo precisa fazer o primeiro pedido ou logar na mesa
	'''
    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA)
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key, comanda=comandasession.comanda,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_auto:acessar_autoatendimento')

    if pedido.quantidade_itens == int(
            0):  # Mesmo que haja uma sessão aberta, mas ainda não colocou nada no pedido, permanece no cardápio
        return redirect(
            'onshop_auto:acessar_autoatendimento')  # Se não possui pedido então não é para definir contato ainda

    # Se já tem sessão, mas não tem pedido, é porque está fazendo novo pedido, porém já não precisa entrar no formulário de contato
    try:
        comprador = get_object_or_404(CompradorPedidoAuto, session_key=request.session.session_key)
        pedido.comprador = comprador
        pedido.save()
        return redirect('onshop_auto:confirmacao')
    except:
        pass

    if request.method == 'POST':
        contato = contato_form = ContatoForm(request.POST)

        if contato_form.is_valid():
            # nome = contato_form.cleaned_data['nome']
            telefone = contato_form.cleaned_data['telefone']
            # email = contato_form.cleaned_data['email']

            # comprador = CompradorPedidoAuto.objects.create(session_key=request.session.session_key, nome=nome, telefone=telefone, email=email)
            comprador = CompradorPedidoAuto.objects.create(session_key=request.session.session_key, telefone=telefone)
            pedido.comprador = comprador
            pedido.save()

            return redirect('onshop_auto:confirmacao')

    else:
        contato_form = ContatoForm()

    estabelecimento = Estabelecimento.objects.all()[0]
    total = pedido.total

    mesa = comandasession.comanda.mesa.numero_mesa

    return render(request, 'onshop_auto/contato.html',
                  {'form': contato_form, 'estabelecimento': estabelecimento, 'mesa': mesa,
                   'quantidade': pedido.quantidade_itens, 'total': total})


def confirmacao(request):
    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA)
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key, comanda=comandasession.comanda,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_auto:acessar_autoatendimento')

    estabelecimento = Estabelecimento.objects.all()[0]

    total = pedido.total

    mesa = comandasession.comanda.mesa.numero_mesa

    return render(request, 'onshop_auto/confirmacao.html',
                  {'pedido': pedido, 'estabelecimento': estabelecimento, 'comandasession': comandasession, 'mesa': mesa,
                   'quantidade': pedido.quantidade_itens, 'total': total})


def remover_pedido(request, pedido_id, produtopedido_id, flag=None):
    pedido = get_object_or_404(PedidoAuto, id=pedido_id)
    produtopedido = get_object_or_404(ProdutoPedidoAuto, id=produtopedido_id)

    pedido.produtos.remove(produtopedido)

    pedido.total = pedido.total - produtopedido.total
    pedido.quantidade_itens = pedido.quantidade_itens - produtopedido.quantidade
    pedido.save()

    if flag:  # Controle se é remoção vinda do Carrinho vem com flag '1' ou da página de confirmação
        return redirect('onshop_auto:ver_carrinho')
    else:
        if pedido.quantidade_itens == 0:
            return redirect('onshop_auto:acessar_autoatendimento')
        else:
            return redirect('onshop_auto:confirmacao')


def concluir_pedido(request):
    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA)
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key, comanda=comandasession.comanda,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_auto:acessar_autoatendimento')

    total = pedido.total

    mesa = comandasession.comanda.mesa.numero_mesa

    estabelecimento = Estabelecimento.objects.all()[0]

    pedido.status = PedidoAuto.PEDIDO_NOVO
    pedido.hora_criacao = datetime.now()
    # É possível pegar o comprador por já estar cadastrado no banco
    comprador = get_object_or_404(CompradorPedidoAuto, session_key=request.session.session_key)
    pedido.comprador = comprador
    pedido.save()

    criar_item_pedido(pedido.id)  # Joga o Item pedido para o administrativo na parte das Mesas

    # Soma o total também na Comanda
    comanda = comandasession.comanda
    comanda.total = Decimal(comanda.total) + Decimal(pedido.total)
    comanda.save()

    enviar_notificacao_push(request)

    return render(request, 'onshop_auto/confirmacao_modal.html',
                  {'pedido': pedido, 'estabelecimento': estabelecimento, 'comandasession': comandasession, 'mesa': mesa,
                   'quantidade': pedido.quantidade_itens, 'total': total})


# ------------ Comandas -----------
# ------------ -------------------

@login_required
def ver_comandas(request):
    comandas = Comanda.objects.filter().order_by('-id')

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_auto/comandas_auto.html',
                  {'comandas': comandas, 'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados})


@login_required
def ver_pedidos_comanda(request, id_comanda):
    comanda = get_object_or_404(Comanda, id=id_comanda)
    pedidos = PedidoAuto.objects.filter(comanda=comanda).exclude(status=PedidoAuto.PEDIDO_CARRINHO)

    return render(request, 'onshop_auto/ver_pedidos_comanda.html', {'comanda': comanda, 'pedidos': pedidos})


# ------------ Impressão -----------
# ------------ -------------------
@login_required
def imprimir_pedido_auto(request, id):
    pedido = get_object_or_404(PedidoAuto, id=id)
    estabelecimento = Estabelecimento.objects.all()[0]
    estabelecimento = estabelecimento.nome

    return render(request, 'onshop_auto/imprimir_pedido_auto.html',
                  {'estabelecimento': estabelecimento, 'pedido': pedido})


@login_required
def imprimir_cupom(request, id_comanda):
    comanda = get_object_or_404(Comanda, id=id_comanda)
    estabelecimento = Estabelecimento.objects.all()[0]
    estabelecimento = estabelecimento.nome

    # pedidos = ItemPedidoAuto.objects.filter(comanda=comanda).order_by('comprador.telefone')

    # pedidos = PedidoAuto.objects.filter(comanda=comanda, status=PedidoAuto.PEDIDO_FINALIZADO)

    pedidos = lista_organizadora_cupom_conta(comanda)

    dez_porcento = comanda.total * Decimal(1.1)
    return render(request, 'onshop_auto/pedido_alternativo_auto.html',
                  {'estabelecimento': estabelecimento, 'comanda': comanda, 'pedidos': pedidos,
                   'dezporcento': dez_porcento})


@login_required
def imprimir_qrcode(request, id_mesa):
    mesa = get_object_or_404(Mesa, id=id_mesa)
    estabelecimento = Estabelecimento.objects.all()[0]
    estabelecimento = estabelecimento.nome

    site = request.META['HTTP_HOST'] + '/auto'

    return render(request, 'onshop_auto/impressao_qrcode.html',
                  {'estabelecimento': estabelecimento, 'codigo': mesa.codigo_mesa, 'mesa': mesa, 'site': site})


# ------------ Gerenciamento de Itens Pedidos -----------
# ------------ -------------------
# Funções facilitadores de Mudança de Mesa e etc...

def sortThird(val):
    return val[3]


def lista_organizadora_cupom_conta(comanda):
    lista = []
    try:
        pedidos = ItemPedidoAuto.objects.filter(comanda=comanda).order_by('comprador')
        ultimo_pedido = ItemPedidoAuto.objects.filter(comanda=comanda).order_by('comprador').reverse()[0]
    except:
        return None

    lista_compradores = []
    lista_compradores_unicos = []
    lista_aux = []

    for pedido in pedidos:
        if pedido == ultimo_pedido:  # Se é o último elemento da lista
            lista.append([
                pedido.produto,
                pedido.quantidade,
                pedido.complemento,
                pedido.comprador.telefone,
                pedido.hora_criacao.strftime("%H:%M"),
                pedido.total
            ])
        else:
            lista.append([
                pedido.produto,
                pedido.quantidade,
                pedido.complemento,
                pedido.comprador.telefone,
                pedido.hora_criacao.strftime("%H:%M"),
                pedido.total
            ], )

    lista.sort(key=sortThird)  # Organiza a lista de acordo com o número de telefone

    # Extrai os compradores distintos e valor dos produtos e mais uma lista dos itens pedidos
    valor = Decimal(0)
    for x in lista:
        if x[3] not in lista_compradores_unicos:
            if len(lista_compradores_unicos):  # Se for o primeiro elemento não entra
                lista_compradores.append([lista_compradores_unicos[-1], valor, lista_aux], )
            valor = Decimal(0)
            lista_aux = []
            lista_compradores_unicos.append(x[3], )
        valor = valor + x[5]
        lista_aux.append(x, )
        if x == lista[-1]:  # Se for o último elemento entra
            lista_compradores.append([lista_compradores_unicos[-1], valor, lista_aux])

    return lista_compradores


def criar_item_pedido(pedido):
    pedido = get_object_or_404(PedidoAuto, id=pedido)

    for item in pedido.produtos.all():
        item = ItemPedidoAuto.objects.create(
            comanda=pedido.comanda,
            pedido_atrelado=pedido,
            comprador=pedido.comprador,
            hora_criacao=pedido.hora_criacao,
            hora_atendimento=pedido.hora_atendimento,
            produto=item.produto,
            complemento=item.complemento,
            quantidade=item.quantidade,
            preco_produto=item.preco_produto,
            adicional=item.adicional,
            total=item.total
        )

    return True


@login_required
def remover_item_pedido(request, id_item):
    item = get_object_or_404(ItemPedidoAuto, id=id_item)
    comanda = item.comanda
    mesa = comanda.mesa

    comanda.total = comanda.total - item.total
    comanda.save()

    item.delete()

    return redirect('onshop_auto:ver_detalhes_mesa_aberta', id_mesa=mesa.id)


@login_required
def transferir_item_pedido(request, id_item):
    '''
	O próprio form já trava para não transferir para a própria mesa
	'''
    item = get_object_or_404(ItemPedidoAuto, id=id_item)
    comanda_antiga = item.comanda
    mesa_antiga = comanda_antiga.mesa

    if request.method == 'POST':
        mesa_form = MesaAbertaForm(request.POST, id_mesa=mesa_antiga.id)

        if mesa_form.is_valid():
            nova_mesa = mesa_form.cleaned_data['numero_mesa']
            nova_mesa = get_object_or_404(Mesa, id=nova_mesa)

            nova_comanda = get_object_or_404(Comanda, mesa=nova_mesa, status=Comanda.COMANDA_ABERTA)
            nova_comanda.total = nova_comanda.total + item.total
            nova_comanda.save()

            comanda_antiga.total = comanda_antiga.total - item.total
            comanda_antiga.save()

            item.comanda = nova_comanda
            item.save()

            return redirect('onshop_auto:ver_detalhes_mesa_aberta', id_mesa=mesa_antiga.id)

    else:
        mesa_form = MesaAbertaForm(id_mesa=mesa_antiga.id)

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_auto/mesa_aberta_detalhes_form.html',
                  {'form': mesa_form, 'mesa': mesa_antiga, 'pedido': item, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados})


@login_required
def transferir_mesa_inteira(request, id_mesa):
    mesa = get_object_or_404(Mesa, id=id_mesa, status=Mesa.MESA_ABERTA)

    comanda = get_object_or_404(Comanda, status=Comanda.COMANDA_ABERTA, mesa=mesa)
    itens_pedidos = ItemPedidoAuto.objects.filter(comanda=comanda)

    if request.method == 'POST':
        mesa_form = MesasForm(request.POST, id_mesa=mesa.id)

        if mesa_form.is_valid():
            nova_mesa = mesa_form.cleaned_data['numero_mesa']
            nova_mesa = get_object_or_404(Mesa, id=nova_mesa)

            if nova_mesa.status == Mesa.MESA_FECHADA:
                nova_mesa.status = Mesa.MESA_ABERTA
                nova_mesa.save()

            try:
                nova_comanda = get_object_or_404(Comanda, mesa=nova_mesa,
                                                 status=Comanda.COMANDA_ABERTA)  # Tenta encontrar uma comanda em aberto da Mesa
            except:
                nova_comanda = Comanda.objects.create(mesa=nova_mesa, status=Comanda.COMANDA_ABERTA,
                                                      hora_abertura=datetime.now(),
                                                      total=Decimal(0.0))  # Caso contrário abre uma comanda da Mesa

            itens = ItemPedidoAuto.objects.filter(comanda=comanda)  # Pega todos os itens registrados na mesa

            for item in itens:
                nova_comanda.total = nova_comanda.total + item.total
                nova_comanda.save()

                comanda.total = comanda.total - item.total
                comanda.save()

                item.comanda = nova_comanda
                item.save()

            return redirect('onshop_auto:ver_detalhes_mesa_aberta', id_mesa=mesa.id)

    else:
        mesa_form = MesasForm(id_mesa=mesa.id)

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_auto/transferir_mesa_form.html',
                  {'form': mesa_form, 'mesa': mesa, 'pedidos': itens_pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados})


# ------------ Leitor de Fora do Sistema (Cliente Final) -----------
# ------------ -------------------
def registrar_codigo_fora(request, id_codigo):
    codigo = id_codigo

    try:  # Analisa se esse cara já não participa de uma mesa com uma comanda aberta
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA)
        return redirect('onshop_auto:ver_cardapio', id_comanda=comandasession.comanda.id)
    except:
        pass

    try:
        codigo = get_object_or_404(Codigo, codigo=codigo)
        mesa = get_object_or_404(Mesa, codigo_mesa=codigo)
    except:
        return redirect('onshop_auto:codigo_errado')

    if mesa.status == Mesa.MESA_FECHADA:  # Caso seja a primeira pessoa a abrir a mesa
        mesa.status = Mesa.MESA_ABERTA
        mesa.save()

    try:
        comanda = get_object_or_404(Comanda, mesa=mesa,
                                    status=Comanda.COMANDA_ABERTA)  # Tenta encontrar uma comanda em aberto da Mesa
    except:
        comanda = Comanda.objects.create(mesa=mesa, status=Comanda.COMANDA_ABERTA, hora_abertura=datetime.now(),
                                         total=Decimal(0.0))  # Caso contrário abre uma comanda da Mesa

    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda=comanda)  # Caso já exista a ComandaSession não faz nada
    except:
        request.session.create()  # Cria uma nova sessão
        comandasession = ComandaSession.objects.create(session_key=request.session.session_key, comanda=comanda)

    return redirect('onshop_auto:ver_cardapio', id_comanda=comanda.id)


# ------------ Ajax Mobile (Cliente Final) -----------
# ------------ -------------------

from django.forms.models import model_to_dict
from django.template.loader import render_to_string


def ver_produto_mobile(request):
    id_produto = request.GET.get('id', None)
    produto = get_object_or_404(ProdutoAuto, id=id_produto)
    perguntas = PerguntaAuto.objects.filter(produto=produto)
    form = ProdutoMobileForm(perguntas)

    try:
        auxiliar = produto.atributos.all()[0]
        atributo = auxiliar.nome
    except:
        atributo = None

    context = {
        'produto': model_to_dict(produto),
        'atributo': atributo,
        'form': form,
        'status': 'ok',
        'key': request.session.session_key
    }

    rendered = render_to_string('onshop_auto/produto_mobile.html', context)

    return JsonResponse({'product_snippet': rendered})


def formulario_ajuda(request):
    id_comanda = request.GET.get('id', None)
    comanda = get_object_or_404(Comanda, id=id_comanda)

    form = MensagemAutoForm()

    context = {
        'form': form,
        'status': 'ok',
        'comanda': comanda.id,
        'key': request.session.session_key
    }

    rendered = render_to_string('onshop_auto/formulario_ajuda.html', context)

    return JsonResponse({'product_snippet': rendered})


def formulario_carrinho(request):
    id_comanda = request.GET.get('id', None)
    token = request.GET.get('token', None)
    id_garcom = request.GET.get('id_garcom', None)

    comanda = get_object_or_404(Comanda, id=id_comanda)

    form = ContatoForm()

    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
    except:
        pedido = None

    if token != '0':  # É porque é Garçom
        garcom = get_object_or_404(Garcom, id=id_garcom)
        try:
            comprador = get_object_or_404(CompradorPedidoAuto, session_key=request.session.session_key)
        except:
            comprador = CompradorPedidoAuto.objects.create(session_key=request.session.session_key,
                                                           telefone=garcom.nome)  # Para se diferenciar dos clientes da mesa é colocado o nome do Garçom

        pedido.comprador = comprador
        pedido.save()

        context = {
            'token': token,
            'garcom': garcom,
            'comprador': comprador,
            'status': 'ok',
            'comanda': comanda.id,
            'pedido': pedido,
            'key': request.session.session_key
        }
        rendered = render_to_string('onshop_auto/formulario_carrinho_garcom.html', context)
    else:
        # Buscando para ver se já há uma pessoa cadastrada
        try:
            comprador = get_object_or_404(CompradorPedidoAuto, session_key=request.session.session_key)
        except:
            comprador = None

        context = {
            'form': form,
            'comprador': comprador,
            'status': 'ok',
            'comanda': comanda.id,
            'pedido': pedido,
            'key': request.session.session_key
        }

        rendered = render_to_string('onshop_auto/formulario_carrinho.html', context)

    return JsonResponse({'product_snippet': rendered})


def ver_parcial(request):
    id_comanda = request.GET.get('id', None)
    comanda = get_object_or_404(Comanda, id=id_comanda)

    # pedidos = ItemPedidoAuto.objects.filter(comanda=comanda)
    pedidos = lista_organizadora_cupom_conta(comanda)  # Se não há pedidos, retorna None

    context = {
        'total': comanda.total,
        'status': 'ok',
        'pedidos': pedidos,
        'comanda': comanda.id,
        'key': request.session.session_key
    }

    rendered = render_to_string('onshop_auto/ver_parcial.html', context)

    return JsonResponse({'product_snippet': rendered})


def pedir_encerramento_mesa(request):
    id_comanda = request.GET.get('id', None)
    comanda = get_object_or_404(Comanda, id=id_comanda)
    # TODO: Criar um objeto de mensagem
    MensagemAuto.objects.create(comanda=comanda, mensagem='Pedido de fechamento de Mesa', hora_criacao=datetime.now())

    enviar_notificacao_mensagem(request, eh_ajuda=0)

    endereco = reverse('onshop_auto:ver_avaliacao_modal', kwargs={'id_comanda': comanda.id})
    return JsonResponse({'status': 'ok', 'product_snippet': endereco})


from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def registrar_codigo_ajax(request):
    url_scan = request.GET.get('codigo', None)
    codigo_scan = url_scan.split('/')[-1]  # Pega o último elemento separado do traço

    try:
        codigo = get_object_or_404(Codigo, codigo=codigo_scan)
        mesa = get_object_or_404(Mesa, codigo_mesa=codigo)
    except:
        response = JsonResponse(
            {'status': 'error', 'codigo': codigo_scan, 'product_snippet': 'Esse código de mesa é inválido!'})
        response.status_code = 404
        return response

    if mesa.status == Mesa.MESA_FECHADA:  # Caso seja a primeira pessoa a abrir a mesa
        mesa.status = Mesa.MESA_ABERTA
        mesa.save()

    try:
        comanda = get_object_or_404(Comanda, mesa=mesa,
                                    status=Comanda.COMANDA_ABERTA)  # Tenta encontrar uma comanda em aberto da Mesa
    except:
        comanda = Comanda.objects.create(mesa=mesa, status=Comanda.COMANDA_ABERTA, hora_abertura=datetime.now(),
                                         total=Decimal(0.0))  # Caso contrário abre uma comanda da Mesa

    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda=comanda)  # Caso já exista a ComandaSession não faz nada
    except:
        request.session.create()  # Cria uma nova sessão
        comandasession = ComandaSession.objects.create(session_key=request.session.session_key, comanda=comanda)

    endereco = reverse('onshop_auto:ver_cardapio', kwargs={'id_comanda': comanda.id})
    return JsonResponse({'status': 'ok', 'product_snippet': endereco})


@csrf_exempt
def enviar_pedido_ajuda(request):
    id_comanda = request.GET.get('id', None)
    mensagem = request.GET.get('mensagem', None)
    comanda = get_object_or_404(Comanda, id=id_comanda)
    # TODO: Criar um objeto de mensagem
    if mensagem:
        MensagemAuto.objects.create(comanda=comanda, mensagem=mensagem, hora_criacao=datetime.now())
        enviar_notificacao_mensagem(request, eh_ajuda=1)

        return JsonResponse({'status': 'ok'})
    else:
        response = JsonResponse({'status': 'error'})
        response.status_code = 404
        return response


@csrf_exempt
def inserir_contato(request):
    key = request.GET.get('key', None)
    form_data = request.GET.get('formData', None)
    form_data_list = json.loads(form_data)
    telefone = form_data_list[0].get("value")

    # id_comanda = request.GET.get('id', None)

    comandasession = get_object_or_404(ComandaSession, session_key=key, comanda__status=Comanda.COMANDA_ABERTA)
    pedido = get_object_or_404(PedidoAuto, session_key=key, comanda=comandasession.comanda,
                               status=PedidoAuto.PEDIDO_CARRINHO)

    comprador = CompradorPedidoAuto.objects.create(session_key=request.session.session_key, telefone=telefone)
    pedido.comprador = comprador
    pedido.save()

    endereco = reverse('onshop_auto:concluir_pedido', kwargs={})
    return JsonResponse({'status': 'ok', 'product_snippet': endereco})


@csrf_exempt
def adicionar_pedido(request):
    id_produto = request.GET.get('id', None)
    form_data = request.GET.get('formData', None)
    key = request.GET.get('key', None)

    form_data_list = json.loads(form_data)
    lista_respostas = []
    for dic in form_data_list:
        lista_respostas.append(dic.values())
    '''
	if not request.session.session_key: #Se não possui sessão iniciada, cria-se uma
		request.session.save()
	'''

    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA)
    except:
        return redirect('onshop_auto:acessar_autoatendimento')

    comanda = comandasession.comanda

    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key,
                                   status=PedidoAuto.PEDIDO_CARRINHO)  # Verifica se há pedidos ainda em aberto
    except:
        pedido = PedidoAuto.objects.create(comanda=comanda)

    nome, quantidade_pp = lista_respostas[-1]
    adicional_pp = Decimal(0)  # Calculado através da lista de complementos
    total_pp = Decimal(0)  # Calculado através da lista de complementos
    produto = get_object_or_404(ProdutoAuto, id=id_produto)

    lista_complemento = []
    for x, y in lista_respostas:
        if x.startswith('especial'):  # Campo do pedido especial
            if y:
                lista_complemento.append(['\nPEDIDO ESPECIAL', y])
            break
        if x.startswith('quantity'):  # Campo do pedido quantidade
            # Faz os cálculos finais do Pedido
            # Não precisa ser feito nada, uma vez que já se pega a quantidade pela lista_respostas
            break

        if x.startswith('question_'):
            resposta = get_object_or_404(RespostaAuto, id=y)  # Objeto Resposta está no value
            lista_complemento.append(['\n' + resposta.pergunta.pergunta, resposta.resposta])

            if resposta.preco_adicional:  # A lista de respostas para múltipla e exclusiva só são recebidas quando são respondidas
                # Acrescenta no Pedido
                adicional_pp = adicional_pp + resposta.preco_adicional

        else:  # Se não é pergunta de escolha e nem especial é Resposta Recorrente
            resposta = get_object_or_404(RespostaAuto, id=x)  # Objeto Resposta está no name

            if y != "0":
                complemento = resposta.pergunta.pergunta + ' ' + resposta.resposta
                lista_complemento.append([complemento, y])
                if resposta.preco_adicional:
                    # Acrescenta no Pedido vezes a quantidade do value
                    adicional_pp = adicional_pp + int(y) * resposta.preco_adicional
                    pass

    if produto.preco_promocao:
        total_pp = int(quantidade_pp) * produto.preco_promocao + int(quantidade_pp) * adicional_pp
        preco_pp = produto.preco_promocao
    else:
        total_pp = int(quantidade_pp) * produto.preco + int(quantidade_pp) * adicional_pp
        preco_pp = produto.preco

    produtopedido = ProdutoPedidoAuto.objects.create(produto=produto, quantidade=quantidade_pp, preco_produto=preco_pp,
                                                     adicional=adicional_pp, total=total_pp)
    lista_aux = []
    for i in lista_complemento:
        lista_aux.append(': '.join(i))

    produtopedido.complemento = '<br/>'.join(lista_aux)
    produtopedido.save()

    # Atualizando o Pedido Geral
    pedido.produtos.add(produtopedido)
    pedido.total = Decimal(pedido.total) + Decimal(total_pp)
    pedido.quantidade_itens = pedido.quantidade_itens + int(quantidade_pp)
    pedido.save()

    '''
	
	pedido.quantidade_itens = pedido.quantidade_itens + quantidade_pp
	pedido.save()
	'''
    # produto_pedido = ProdutoPedido.objects.create(produto=produto)
    # Pega as informações complementares
    # Pega o valor de quantidade
    # Faz o cálculo do pedido
    # Insere no Pedido do Carrinho

    return JsonResponse({'status': 'ok', 'quantidade': pedido.quantidade_itens, 'total': pedido.total})


# return JsonResponse({'status': 'ok', 'produto': id_produto, 'formData': form_data, 'lista': lista_respostas, 'session_key': session_key, 'key': key, 'lista_complemento': lista_complemento, 'quantidade': pedido.quantidade_itens, 'total': pedido.total })


# ------------ Envio Notificação Push -----------
# ------------ -------------------
import requests  # pip install requests
import json


def enviar_notificacao_push(request):
    auxiliar = PushSignal.objects.all()[0]
    authorization = auxiliar.authorization
    app_id = auxiliar.app_id

    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic " + authorization}

    payload = {"app_id": app_id,
               "included_segments": ["All"],
               "url": request.scheme + request.META['HTTP_HOST'] + "/auto/painel/novos-pedidos/",
               "headings": {"en": "Novo pedido chegando AUTOATENDIMENTO", "pt": "Novo pedido chegando AUTOATENDIMENTO"},
               "contents": {"en": "Foi realizado um novo pedido no AUTOATENDIMENTO!",
                            "pt": "Foi realizado um novo pedido no AUTOATENDIMENTO!"}}

    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

    # print(req.status_code, req.reason)
    return True


def enviar_notificacao_mensagem(request, eh_ajuda):
    auxiliar = PushSignal.objects.all()[0]
    authorization = auxiliar.authorization
    app_id = auxiliar.app_id

    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic " + authorization}

    if eh_ajuda:
        payload = {"app_id": app_id,
                   "included_segments": ["All"],
                   "url": request.scheme + request.META['HTTP_HOST'] + "/auto/painel/ver-mensagens/",
                   "headings": {"en": "Mensagem de pedido de ajuda chegando", "pt": "Nova mensagem de Ajuda chegando!"},
                   "contents": {"en": "Mensagem de pedido de ajuda chegando!",
                                "pt": "Chegou uma nova mensagem de Ajuda!"}}
    else:
        payload = {"app_id": app_id,
                   "included_segments": ["All"],
                   "url": request.scheme + request.META['HTTP_HOST'] + "/auto/painel/ver-mensagens/",
                   "headings": {"en": "Pedido de fechamento de Mesa chegando",
                                "pt": "Pedido de fechamento de Mesa chegando!"},
                   "contents": {"en": "Fechamento de Mesa!", "pt": "Pedido de fechamento de Mesa chegando!"}}

    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

    # print(req.status_code, req.reason)
    return True


# ------------ Administrativo de Pedidos -----------
# ------------ -------------------
@login_required
def novos_pedidos_auto(request):
    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/novos_pedidos_auto.html',
                  {'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def pedidos_andamento(request):
    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos.count()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/pedidos_andamento.html',
                  {'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def pedidos_finalizados(request):
    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO).order_by('-hora_criacao')
    qtde_pedidos_finalizados = pedidos.count()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/pedidos_finalizados.html',
                  {'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def ver_mensagens(request):
    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO).order_by('-hora_criacao')
    qtde_pedidos_finalizados = pedidos.count()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    return render(request, 'onshop_auto/mensagens_auto.html',
                  {'mensagens': mensagens, 'pedidos': pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def mensagem_atendida(request, id_mensagem):
    mensagem = get_object_or_404(MensagemAuto, id=id_mensagem)

    mensagem.status = MensagemAuto.MENSAGEM_ATENDIDA
    mensagem.save()

    return redirect('onshop_auto:ver_mensagens')


@login_required
def finalizar_pedido(request, id):
    pedido = get_object_or_404(PedidoAuto, status=PedidoAuto.PEDIDO_ANDAMENTO, id=id)

    pedido.status = PedidoAuto.PEDIDO_FINALIZADO
    pedido.save()

    return redirect('onshop_auto:ver_pedido_finalizado', id=pedido.id)


@login_required
def ver_pedido(request, id):
    try:
        pedido = get_object_or_404(PedidoAuto, status=PedidoAuto.PEDIDO_NOVO,
                                   id=id)  # Se não for novo está em andamento
    except:
        pedido = get_object_or_404(PedidoAuto, status=PedidoAuto.PEDIDO_ANDAMENTO, id=id)

    if pedido.status == PedidoAuto.PEDIDO_NOVO:
        pedido.status = PedidoAuto.PEDIDO_ANDAMENTO
        pedido.hora_atendimento = datetime.now()
        pedido.save()

    # Tirei daqui e estou colocando na função concluir_pedido
    # criar_item_pedido(pedido.id) #Monta o Item pedido para o administrativo

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos.count()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    return render(request, 'onshop_auto/ver_pedido.html', {'pedido': pedido, 'qtde_novos_pedidos': qtde_novos_pedidos,
                                                           'qtde_pedidos_andamento': qtde_pedidos_andamento,
                                                           'qtde_pedidos_finalizados': qtde_pedidos_finalizados})


@login_required
def rejeitar_pedido(request, pedido_id=None):
    try:
        pedido = get_object_or_404(PedidoAuto, status=PedidoAuto.PEDIDO_NOVO,
                                   id=pedido_id)  # Se não for novo está em andamento
    except:
        pedido = get_object_or_404(PedidoAuto, status=PedidoAuto.PEDIDO_ANDAMENTO, id=pedido_id)

    comanda = pedido.comanda
    total = pedido.total
    comanda.total = comanda.total - total
    comanda.save()

    pedido.status = PedidoAuto.PEDIDO_REJEITADO
    pedido.save()

    # Retira item a item do administrativo
    # Como já foi incluído o item na hora do pedido, é garantido que o item seja encontrado
    itens_incluidos = ItemPedidoAuto.objects.filter(comanda=pedido.comanda, pedido_atrelado=pedido)

    for item in itens_incluidos:
        item.delete()

    return redirect('onshop_auto:novos_pedidos_auto')


@login_required
def ver_pedido_finalizado(request, id):
    pedido = get_object_or_404(PedidoAuto, status=PedidoAuto.PEDIDO_FINALIZADO, id=id)

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos.count()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    return render(request, 'onshop_auto/ver_pedido_finalizado.html',
                  {'pedido': pedido, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados})


@login_required
def fechar_mesa(request, id_mesa):
    mesa = get_object_or_404(Mesa, id=id_mesa, status=Mesa.MESA_ABERTA)

    comanda = get_object_or_404(Comanda, status=Comanda.COMANDA_ABERTA, mesa=mesa)

    # TODO: Verificar se há ainda pedidos pendentes para a Mesa
    pedidos = PedidoAuto.objects.filter(Q(status=PedidoAuto.PEDIDO_NOVO) | Q(status=PedidoAuto.PEDIDO_ANDAMENTO))

    for pedido in pedidos:  # Por enquanto joga os pedidos no limbo
        pedido.status = PedidoAuto.PEDIDO_CARRINHO
        pedido.save()

    # TODO: Enviar mensagem informando sobre pedidos pendentes

    mesa.status = Mesa.MESA_FECHADA
    mesa.save()

    comanda.status = Comanda.COMANDA_FECHADA
    comanda.hora_fechamento = datetime.now()
    comanda.save()

    # TODO: Enviar mensagem

    return redirect('onshop_auto:ver_mesas_abertas')


# ------------ Administrativo de Avaliações -----------
# ------------ -------------------
def ver_avaliacoes(request):
    try:  # Se ainda não existe, cria. Como o modelo já possui default para os campos não ha problemas
        q_avaliado = QAvaliado.objects.all()[0]
    except:
        q_avaliado = QAvaliado.objects.create()

    pedidos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    if request.method == 'POST':
        avaliacao = avaliacao_form = AvaliacaoForm(request.POST, instance=q_avaliado)

        if avaliacao_form.is_valid():
            avaliacao = avaliacao_form.save()
            avaliacao.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_avaliacoes')

    else:
        avaliacao_form = AvaliacaoForm(instance=q_avaliado)

    avaliacoes = Avaliacao.objects.all().order_by('-hora_criacao')[:10]

    return render(request, 'onshop_auto/avaliacoes.html',
                  {'q_avaliado': q_avaliado, 'form': avaliacao_form, 'pedidos': pedidos,
                   'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens,
                   'avaliacoes': avaliacoes})


# ------------ Avaliações Usuário Final -----------
# ------------ -------------------
def ver_avaliacao_modal(request, id_comanda):
    # A comanda é necessária somente para depois encaminhar para o cardápio correto
    comanda = get_object_or_404(Comanda, id=id_comanda)

    try:  # Se ainda não existe, cria. Como o modelo já possui default para os campos não ha problemas
        q_avaliado = QAvaliado.objects.all()[0]
    except:
        q_avaliado = QAvaliado.objects.create()

    if request.method == 'POST':
        avaliacao = avaliacao_form = NotaAvaliacaoForm(request.POST)

        if avaliacao_form.is_valid():
            avaliacao = avaliacao_form.save()
            avaliacao.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_avaliacoes')

    else:
        avaliacao_form = NotaAvaliacaoForm()

    return render(request, 'onshop_auto/avaliacao_modal.html',
                  {'form': avaliacao_form, 'q_avaliado': q_avaliado, 'comanda': comanda})


@csrf_exempt
def receber_avaliacao(request):
    key = request.GET.get('key', None)
    p_campo = request.GET.get('p_campo', None)
    s_campo = request.GET.get('s_campo', None)
    t_campo = request.GET.get('t_campo', None)
    q_campo = request.GET.get('q_campo', None)

    msg_data = request.GET.get('msgData', None)
    msg_data_list = json.loads(msg_data)
    mensagem = msg_data_list[0].get("value")
    form_data_list = mensagem
    fuso_local = pytz.timezone('America/Sao_Paulo')

    Avaliacao.objects.create(
        nota_primeiro_campo=p_campo,
        nota_segundo_campo=s_campo,
        nota_terceiro_campo=t_campo,
        nota_quarto_campo=q_campo,
        mensagem=mensagem,
        hora_criacao=datetime.now(fuso_local)
    )

    # endereco = reverse('onshop_auto:ver_cardapio', kwargs={'id_comanda': comanda.id})
    return JsonResponse({'status': 'ok'})


# ------------ Complementos -----------
# ------------ -------------------
@login_required
def adicionar_complemento(request, id):
    produto = get_object_or_404(ProdutoAuto, id=id)
    perguntas = PerguntaAuto.objects.filter(produto=produto)

    return render(request, 'onshop_auto/complementos.html', {'produto': produto, 'perguntas': perguntas})


@login_required
def adicionar_pergunta(request, id, id_pergunta=None):
    produto = get_object_or_404(ProdutoAuto, id=id)

    if id_pergunta:
        auxiliar = get_object_or_404(PerguntaAuto, id=id_pergunta)

    if request.method == 'POST':
        if id_pergunta:
            pergunta = pergunta_form = PerguntaForm(request.POST, request.FILES, instance=auxiliar)
        else:
            pergunta = pergunta_form = PerguntaForm(request.POST, request.FILES)

        if pergunta_form.is_valid():
            pergunta = pergunta_form.save(commit=False)
            pergunta.produto = produto
            pergunta.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:adicionar_complemento_auto', id=produto.id)
    else:
        if id_pergunta:
            pergunta_form = PerguntaForm(instance=auxiliar)
        else:
            pergunta_form = PerguntaForm()

    return render(request, 'onshop_auto/perguntas.html', {'produto': produto, 'form': pergunta_form})


@login_required
def ver_respostas(request, id_pergunta):
    pergunta = get_object_or_404(PerguntaAuto, id=id_pergunta)
    produto = pergunta.produto
    respostas = RespostaAuto.objects.filter(pergunta=pergunta)

    return render(request, 'onshop_auto/respostas.html',
                  {'produto': produto, 'pergunta': pergunta, 'respostas': respostas})


@login_required
def adicionar_resposta(request, id_pergunta, id_resposta=None):
    pergunta = get_object_or_404(PerguntaAuto, id=id_pergunta)
    produto = pergunta.produto

    if id_resposta:
        auxiliar = get_object_or_404(RespostaAuto, id=id_resposta)

    if request.method == 'POST':
        if id_resposta:
            resposta = resposta_form = RespostaForm(request.POST, request.FILES, instance=auxiliar)
        else:
            resposta = resposta_form = RespostaForm(request.POST, request.FILES)

        if resposta_form.is_valid():
            resposta = resposta_form.save(commit=False)
            resposta.pergunta = pergunta
            resposta.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_respostas_auto', id_pergunta=pergunta.id)
    else:
        if id_resposta:
            resposta_form = RespostaForm(instance=auxiliar)
        else:
            resposta_form = RespostaForm()

    return render(request, 'onshop_auto/form_resposta.html',
                  {'produto': produto, 'pergunta': pergunta, 'form': resposta_form})


@login_required
def deletar_pergunta(request, id_pergunta):
    '''
	Deleta também as respostas
	'''
    pergunta = get_object_or_404(PerguntaAuto, id=id_pergunta)
    produto = pergunta.produto
    respostas = RespostaAuto.objects.filter(pergunta=pergunta)

    for resposta in respostas:
        resposta.delete()

    pergunta.delete()

    # TODO: Enviar Mensagem

    return redirect('onshop_auto:adicionar_complemento_auto', id=produto.id)


@login_required
def deletar_resposta(request, id_resposta):
    resposta = get_object_or_404(RespostaAuto, id=id_resposta)
    pergunta = resposta.pergunta

    resposta.delete()

    # TODO: Enviar Mensagem

    return redirect('onshop_auto:ver_respostas_auto', id_pergunta=pergunta.id)


# ------------ Complementos Modelo -----------
# ------------ -------------------
@login_required
def ver_complementos(request):
    complementos = ComplementoModeloAuto.objects.all()

    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_entregues = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_entregues.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    return render(request, 'onshop_auto/lista_complementos_modelo.html',
                  {'complementos': complementos, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def ver_lista_complemento(request, id=id):
    complemento_modelo = get_object_or_404(ComplementoModeloAuto, id=id)
    perguntas_modelo = PerguntaModeloAuto.objects.filter(modelo=complemento_modelo)

    return render(request, 'onshop_auto/ver_lista_complementos_modelo.html',
                  {'complemento': complemento_modelo, 'perguntas': perguntas_modelo})


@login_required
def editar_complementos(request, id=None):
    if id:
        auxiliar = get_object_or_404(ComplementoModeloAuto, id=id)

    if request.method == 'POST':
        if id:
            modelo = modelo_form = ComplementoModeloForm(request.POST, request.FILES, instance=auxiliar)
        else:
            modelo = modelo_form = ComplementoModeloForm(request.POST, request.FILES)

        if modelo_form.is_valid():
            modelo = modelo_form.save(commit=False)
            modelo.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_lista_complemento_auto', id=modelo.id)
    else:
        if id:
            modelo_form = ComplementoModeloForm(instance=auxiliar)
        else:
            modelo_form = ComplementoModeloForm()

    return render(request, 'onshop_auto/editar_complementos_modelo.html', {'form': modelo_form})


@login_required
def adicionar_pergunta_modelo(request, id, id_pergunta=None):
    modelo = get_object_or_404(ComplementoModeloAuto, id=id)

    if id_pergunta:
        auxiliar = get_object_or_404(PerguntaModeloAuto, id=id_pergunta)

    if request.method == 'POST':
        if id_pergunta:
            pergunta = pergunta_form = PerguntaModeloForm(request.POST, request.FILES, instance=auxiliar)
        else:
            pergunta = pergunta_form = PerguntaModeloForm(request.POST, request.FILES)

        if pergunta_form.is_valid():
            pergunta = pergunta_form.save(commit=False)
            pergunta.modelo = modelo
            pergunta.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_lista_complemento_auto', id=modelo.id)
    else:
        if id_pergunta:
            pergunta_form = PerguntaModeloForm(instance=auxiliar)
        else:
            pergunta_form = PerguntaModeloForm()

    return render(request, 'onshop_auto/perguntas_modelo.html', {'complemento': modelo, 'modelo': modelo,
                                                                 'form': pergunta_form})  # Só para poder pegar a url de quem ele herda


@login_required
def deletar_complemento_modelo(request, id=None):
    '''
	Deleta Perguntas e Respostas Modelo
	'''
    modelo = get_object_or_404(ComplementoModeloAuto, id=id)

    perguntas = PerguntaModeloAuto.objects.filter(modelo=modelo)

    for pergunta in perguntas:
        deletar_pergunta_modelo(id_pergunta=pergunta.id)

    modelo.delete()

    return redirect('onshop_auto:ver_complementos_auto')


@login_required
def deletar_pergunta_modelo(request, id_pergunta):
    '''
	Deleta também as respostas
	'''
    pergunta = get_object_or_404(PerguntaModeloAuto, id=id_pergunta)
    modelo = pergunta.modelo
    respostas = RespostaModeloAuto.objects.filter(pergunta=pergunta)

    for resposta in respostas:
        resposta.delete()

    pergunta.delete()

    # TODO: Enviar Mensagem

    return redirect('onshop_auto:ver_lista_complemento_auto', id=modelo.id)


@login_required
def ver_respostas_modelo(request, id_pergunta):
    pergunta = get_object_or_404(PerguntaModeloAuto, id=id_pergunta)
    modelo = pergunta.modelo
    respostas = RespostaModeloAuto.objects.filter(pergunta=pergunta)

    return render(request, 'onshop_auto/respostas_modelo.html',
                  {'complemento': modelo, 'modelo': modelo, 'pergunta': pergunta, 'respostas': respostas})


@login_required
def adicionar_resposta_modelo(request, id_pergunta, id_resposta=None):
    pergunta = get_object_or_404(PerguntaModeloAuto, id=id_pergunta)
    modelo = pergunta.modelo

    if id_resposta:
        auxiliar = get_object_or_404(RespostaModeloAuto, id=id_resposta)

    if request.method == 'POST':
        if id_resposta:
            resposta = resposta_form = RespostaModeloForm(request.POST, request.FILES, instance=auxiliar)
        else:
            resposta = resposta_form = RespostaModeloForm(request.POST, request.FILES)

        if resposta_form.is_valid():
            resposta = resposta_form.save(commit=False)
            resposta.pergunta = pergunta
            resposta.save()
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_respostas_modelo_auto', id_pergunta=pergunta.id)
    else:
        if id_resposta:
            resposta_form = RespostaModeloForm(instance=auxiliar)
        else:
            resposta_form = RespostaModeloForm()

    return render(request, 'onshop_auto/form_resposta_modelo.html',
                  {'complemento': modelo, 'modelo': modelo, 'pergunta': pergunta, 'form': resposta_form})


@login_required
def deletar_resposta_modelo(request, id_resposta):
    resposta = get_object_or_404(RespostaModeloAuto, id=id_resposta)

    pergunta = resposta.pergunta

    resposta.delete()

    return redirect('onshop_auto:ver_respostas_modelo_auto', id_pergunta=pergunta.id)


@login_required
def atribuir_produtos(request, complemento_id):
    '''
	Substitui as perguntas existentes pelas do Modelo
	'''
    complemento = get_object_or_404(ComplementoModeloAuto, id=complemento_id)
    perguntas_modelo = PerguntaModeloAuto.objects.filter(modelo=complemento)

    if request.method == 'POST':
        produtos = atribuir_form = AtribuirForm(request.POST, request.FILES)

        if atribuir_form.is_valid():
            # atribuidos = request.POST.getlist('produtos') #Pega todos os values dos produtos setados
            atribuidos = atribuir_form.cleaned_data['produtos']

            for x in atribuidos:
                produto = get_object_or_404(ProdutoAuto, id=x)
                perguntas = PerguntaAuto.objects.filter(produto=produto)
                # Faz a deleção das perguntas e respostas existentes
                for pergunta in perguntas:
                    deletar_pergunta(request, pergunta.id)
                # Faz a substituição pelas perguntas e respostas do modelo
                for pergunta in perguntas_modelo:
                    pergunta_atribuida = PerguntaAuto.objects.create(produto=produto, pergunta=pergunta.pergunta,
                                                                     tipo=pergunta.tipo, limite=pergunta.limite)
                    respostas_modelo = RespostaModeloAuto.objects.filter(pergunta=pergunta)
                    for resposta in respostas_modelo:
                        resposta_atribuida = RespostaAuto.objects.create(pergunta=pergunta_atribuida, resposta=resposta,
                                                                         preco_adicional=resposta.preco_adicional)
            # Faz a atribuição
            # TODO: Enviar Mensagem

            return redirect('onshop_auto:ver_lista_complemento_auto', id=complemento.id)

    else:
        atribuir_form = AtribuirForm()

    return render(request, 'onshop_auto/atribuir_form.html',
                  {'complemento': complemento, 'perguntas': perguntas_modelo, 'form': atribuir_form})


# -------- Funções de Controle --------------

@csrf_exempt
def analisa_pedido_auto(request):
    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
        total = pedido.total
    except:
        response = JsonResponse(
            {'status': 'error', 'product_snippet': 'Blau! Não é possível fazer o pedido nesse momento!'})
        response.status_code = 404
        return response

    verifica_horario()

    estabelecimento = Estabelecimento.objects.all()[0]
    pedido_minimo = estabelecimento.pedido_minimo

    if estabelecimento.status == Estabelecimento.FECHADO:
        response = JsonResponse(
            {'status': 'error', 'product_snippet': 'O estabelecimento se encontra fechado nesse momento!'})
        response.status_code = 404
        return response

    p_etapa = reverse('onshop_auto:contato')
    return JsonResponse({'status': 'ok', 'product_snippet': p_etapa})


def verifica_horario():
    try:
        estabelecimento = Estabelecimento.objects.all()[0]
    except:
        estabelecimento = Estabelecimento.objects.create(nome='OnShop')

    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
        quantidade = pedido.quantidade_itens
        total = pedido.total
    except:
        quantidade = 0
        total = 0.00

    fuso_local = pytz.timezone('America/Sao_Paulo')
    hora_acesso = datetime.now(fuso_local).time()
    if estabelecimento.horario_abertura < estabelecimento.horario_fechamento:  # Significa que abre e fecha no mesmo dia
        if hora_acesso > estabelecimento.horario_abertura and hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    else:  # Significa que abre e fecha no dia seguinte
        if hora_acesso > estabelecimento.horario_abertura or hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    estabelecimento.save()

    return True


# -------- Administrativo Garçom --------------
@login_required
def ver_garcons(request):
    pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_entregues = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_entregues.count()

    mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
    qtde_mensagens = mensagens.count()

    garcons = Garcom.objects.all()

    return render(request, 'onshop_auto/garcons_auto.html',
                  {'garcons': garcons, 'qtde_novos_pedidos': qtde_novos_pedidos,
                   'qtde_pedidos_andamento': qtde_pedidos_andamento,
                   'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def editar_garcons(request, id=None):
    aux = None
    if id:
        aux = get_object_or_404(Garcom, id=id)

    if request.method == 'POST':
        if id:
            garcom = garcom_form = GarcomForm(request.POST, instance=aux)
        else:
            garcom = garcom_form = GarcomForm(request.POST)

        if garcom_form.is_valid():
            garcom.save()

        return redirect('onshop_auto:ver_garcons_auto')
    else:
        if id:
            garcom_form = GarcomForm(instance=aux)
        else:
            garcom_form = GarcomForm()

        pedidos_novos = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_NOVO)
        qtde_novos_pedidos = pedidos_novos.count()

        pedidos_andamento = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_ANDAMENTO)
        qtde_pedidos_andamento = pedidos_andamento.count()

        pedidos_entregues = PedidoAuto.objects.filter(status=PedidoAuto.PEDIDO_FINALIZADO)
        qtde_pedidos_finalizados = pedidos_entregues.count()

        mensagens = MensagemAuto.objects.filter(status=MensagemAuto.MENSAGEM_NAO_ATENDIDA).order_by('-hora_criacao')
        qtde_mensagens = mensagens.count()

        return render(request, 'onshop_auto/form_garcom.html',
                      {'form': garcom_form, 'qtde_novos_pedidos': qtde_novos_pedidos,
                       'qtde_pedidos_andamento': qtde_pedidos_andamento,
                       'qtde_pedidos_finalizados': qtde_pedidos_finalizados, 'qtde_mensagens': qtde_mensagens})


@login_required
def deletar_garcom(request, id):
    garcom = get_object_or_404(Garcom, id=id)
    garcom.delete()

    return redirect('onshop_auto:ver_garcons_auto')


# -------- Funções de Garçom --------------
def atendimento_garcom(request):
    novo_token = randint(0, 9999999999)

    if request.method == 'POST':
        form = AtendimentoForm(request.POST)

        if form.is_valid():
            try:
                usuario = request.POST['usuario']
                senha = request.POST['senha']
                garcom = get_object_or_404(Garcom, usuario=form.cleaned_data['usuario'],
                                           senha=form.cleaned_data['senha'])
                garcom.token = novo_token
                garcom.save()

                return redirect(
                    reverse('onshop_auto:atendimento_mesas', kwargs={'id_garcom': garcom.id, 'token': garcom.token}))

            except Exception as e:
                return render(request, 'onshop_auto/atendimento.html',
                              {'form': form, 'login_error': 'Usuário e/ou senha incorretos'})

        return render(request, 'onshop_auto/atendimento.html', {'form': form})
    else:
        form = AtendimentoForm()

    return render(request, 'onshop_auto/atendimento.html', {'form': form})


def sair_garcom(request, id_garcom, token):
    garcom = get_object_or_404(Garcom, id=id_garcom)

    if token != garcom.token:  # Se o token de segurança for diferente do token enviado joga para a página de login de Garçom novamente
        return redirect('onshop_auto:atendimento_garcom')

    garcom.token = ''
    garcom.save()

    return redirect('onshop_auto:atendimento_garcom')


def atendimento_mesas(request, id_garcom, token, codigo=None):  # O código é apenas para quando se clicar em alguma mesa
    garcom = get_object_or_404(Garcom, id=id_garcom)

    if token != garcom.token:  # Se o token de segurança for diferente do token enviado joga para a página de login de Garçom novamente
        return redirect('onshop_auto:atendimento_garcom')

    if codigo:
        mesa = get_object_or_404(Mesa, numero_mesa=codigo)

        if mesa.status == Mesa.MESA_FECHADA:  # Caso seja a primeira pessoa a abrir a mesa
            mesa.status = Mesa.MESA_ABERTA
            mesa.save()

        try:
            comanda = get_object_or_404(Comanda, mesa=mesa,
                                        status=Comanda.COMANDA_ABERTA)  # Tenta encontrar uma comanda em aberto da Mesa
        except:
            comanda = Comanda.objects.create(mesa=mesa, status=Comanda.COMANDA_ABERTA, hora_abertura=datetime.now(),
                                             total=Decimal(0.0))  # Caso contrário abre uma comanda da Mesa

        try:
            get_object_or_404(ComandaSession, session_key=request.session.session_key,
                              comanda=comanda)  # Caso já exista a ComandaSession não faz nada
        except:
            request.session.create()  # Cria uma nova sessão
            ComandaSession.objects.create(session_key=request.session.session_key, comanda=comanda)

        return redirect(reverse('onshop_auto:ver_cardapio_garcom',
                                kwargs={'id_comanda': comanda.id, 'id_garcom': garcom.id, 'token': token}))

    mesas = Mesa.objects.all()

    return render(request, 'onshop_auto/atendimento_mesas.html',
                  {'mesas': mesas, 'garcom': garcom, 'token': garcom.token})


def ver_cardapio_garcom(request, id_comanda, id_garcom, token):
    garcom = get_object_or_404(Garcom, id=id_garcom)

    if token != garcom.token:  # Se o token de segurança for diferente do token enviado joga para a página de login de Garçom novamente
        return redirect('onshop_auto:atendimento_garcom')

    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key,
                                           comanda__status=Comanda.COMANDA_ABERTA, comanda__id=id_comanda)
    except:
        return redirect('onshop_auto:atendimento_mesas', id_garcom=garcom.id, token=token)

    categorias = CategoriaAuto.objects.all()
    lista = []
    for categoria in categorias:
        produtos = ProdutoAuto.objects.filter(categoria=categoria)
        lista.append([categoria, produtos])

    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
        quantidade = pedido.quantidade_itens
        total = pedido.total
    except:
        pedido = PedidoAuto.objects.create(comanda=comandasession.comanda, session_key=request.session.session_key,
                                           status=PedidoAuto.PEDIDO_CARRINHO)
        quantidade = 0
        total = 0.00

    try:
        estabelecimento = Estabelecimento.objects.all()[0]
    except:
        estabelecimento = Estabelecimento.objects.create(nome='OnShop')

    fuso_local = pytz.timezone('America/Sao_Paulo')
    hora_acesso = datetime.now(fuso_local).time()
    if estabelecimento.horario_abertura < estabelecimento.horario_fechamento:  # Significa que abre e fecha no mesmo dia
        if hora_acesso > estabelecimento.horario_abertura and hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    else:  # Significa que abre e fecha no dia seguinte
        if hora_acesso > estabelecimento.horario_abertura or hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO

    estabelecimento.save()

    mesa = comandasession.comanda.mesa.numero_mesa

    return render(request, 'onshop_auto/cardapio.html',
                  {'lista': lista, 'mesa': mesa, 'estabelecimento': estabelecimento, 'quantidade': quantidade,
                   'total': total, 'comanda': id_comanda, 'categorias': categorias, 'token': token, 'garcom': garcom,
                   'id_garcom': garcom.id})


def formulario_carrinho_garcom(request, id_comanda, id_garcom, token):
    comanda = get_object_or_404(Comanda, id=id_comanda)

    try:
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
    except:
        pedido = None

    # Buscando para ver se já há uma pessoa cadastrada, mesmo sendo Garçom
    try:
        comprador = get_object_or_404(CompradorPedidoAuto, session_key=request.session.session_key)
    except:
        garcom = get_object_or_404(Garcom, id=id_garcom)
        comprador = CompradorPedidoAuto.objects.create(session_key=request.session.session_key,
                                                       telefone=garcom.nome)  # Para se diferenciar dos clientes da mesa é colocado o nome do Garçom

    context = {
        'token': token,
        'id_garcom': id_garcom,
        'comprador': comprador,
        'status': 'ok',
        'comanda': comanda.id,
        'pedido': pedido,
        'key': request.session.session_key
    }

    rendered = render_to_string('onshop_auto/formulario_carrinho_garcom.html', context)

    return JsonResponse({'product_snippet': rendered})


def concluir_pedido_garcom(request, id_comanda, id_garcom, token):
    garcom = get_object_or_404(Garcom, id=id_garcom)

    if token != garcom.token:  # Se o token de segurança for diferente do token enviado joga para a página de login de Garçom novamente
        return redirect('onshop_auto:atendimento_garcom')

    comanda = get_object_or_404(Comanda, id=id_comanda)

    try:
        comandasession = get_object_or_404(ComandaSession, session_key=request.session.session_key, comanda=comanda,
                                           comanda__status=Comanda.COMANDA_ABERTA)
        pedido = get_object_or_404(PedidoAuto, session_key=request.session.session_key, comanda=comanda,
                                   status=PedidoAuto.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_auto:atendimento_mesas', id_garcom=garcom.id, token=garcom.token)

    total = pedido.total

    mesa = comanda.mesa.numero_mesa

    estabelecimento = Estabelecimento.objects.all()[0]

    pedido.status = PedidoAuto.PEDIDO_NOVO
    pedido.hora_criacao = datetime.now()
    pedido.save()

    criar_item_pedido(pedido.id)  # Joga o Item pedido para o administrativo na parte das Mesas

    # Soma o total também na Comanda
    comanda.total = Decimal(comanda.total) + Decimal(pedido.total)
    comanda.save()

    enviar_notificacao_push(request)

    return render(request, 'onshop_auto/confirmacao_modal_garcom.html',
                  {'pedido': pedido, 'estabelecimento': estabelecimento, 'comandasession': comandasession, 'mesa': mesa,
                   'quantidade': pedido.quantidade_itens, 'total': total, 'id_garcom': garcom.id,
                   'token': garcom.token})
