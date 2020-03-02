# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View #Para poder mexer com o Ajax nos produtos
from django.http import JsonResponse
from decimal import Decimal
from datetime import datetime
import pytz #Apenas para poder usar o timezone
from django.urls import reverse

from django.contrib import messages
from .models import Categoria, Atributo, Produto, Estabelecimento, Pergunta, Resposta, ComplementoModelo, PerguntaModelo, RespostaModelo, Pedido, ProdutoPedido, CompradorPedido, LocalRetiradaPedido, OpcaoPagamento, BairrosAtendidos, Relatorio, PushSignal, PPedidos, PMesa, PFormasPag, PPedidosFormaPag, PProduto
from .forms import CategoriaForm, AtributoForm, ProdutoForm, EstabelecimentoForm, PerfilForm, PerguntaForm, RespostaForm, ProdutoMobileForm, ComplementoModeloForm, PerguntaModeloForm, RespostaModeloForm, AtribuirForm, ContatoForm, LocalRetiradaPedidoForm, BairroForm, AcessarForm, PushSignalForm, PMesaModelForm, PProdutoModelForm, PFormasPagModelForm, PPedidosFormaPagModelForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def p_mesas(request):
    form = PMesaModelForm()
    mesas = PMesa.objects.all()

    if request.method == 'POST':
        form = PMesaModelForm(request.POST)
        if form.is_valid():
            form.save()
            form = PMesaModelForm()
            messages.success(request, 'Mesa Salva com Sucesso!')
            return render(request, 'onshop_core/p_mesas.html', {'form': form, 'mesas': mesas})
        else:
            form = PMesaModelForm()
            messages.error(request, 'Erro ao salvar mesa')
            return render(request, 'onshop_core/p_mesas.html', {'form': form, 'mesas': mesas})
    else:
        form = PMesaModelForm()
        return render(request, 'onshop_core/p_mesas.html', {'form': form, 'mesas': mesas})


def forma_pag(request):
    if str(request.method) == 'POST':
        form = PFormasPagModelForm(request.POST)
        if form.is_valid():
            form = form.save()
            form = PFormasPagModelForm()
        else:
            form = PFormasPagModelForm()
    else:
        form = PFormasPagModelForm()

    context = {
        'form': form,
        'formas': PFormasPag.objects.all()
    }
    return render(request, 'onshop_core/forma_pag.html', context)

def p_produtos(request):
    if request.method == 'POST':
        form = PProdutoModelForm(request.POST)
        if form.is_valid():
            form = form.save()
            form = PProdutoModelForm()
        else:
            form = PProdutoModelForm()
    else:
        form = PProdutoModelForm()

    context = {
        'form': form,
        'produtos': PProduto.objects.all()
    }
    return render(request, 'onshop_core/p_produtos.html', context)

def p_pedidos_pag(request):
    if request.method == 'POST':
        form = PPedidosFormaPagModelForm(request.POST)
        if form.is_valid():
            form = form.save()
            form = PPedidosFormaPagModelForm()
        else:
            form = PPedidosFormaPagModelForm()
    else:
        form = PPedidosFormaPagModelForm()

    context = {
        'form': form,
        'pedidos': PPedidosFormaPag.objects.all()
    }
    return render(request, 'onshop_core/p_pedido_pag.html', context)

def p_painel(request):
    metodos = PFormasPag.objects.all()
    pedidos = PPedidosFormaPag.objects.all()

    lista = []

    count = 0

    for metodo in metodos:
        for pedido in pedidos:
            if metodo.forma == pedido.forma:
                count = count + pedido.valor
        if not count==0:
            lista.append([metodo, count])
        count = 0

    print(lista)

    return render(request, 'onshop_core/p_painel.html', {'lista': lista})

def cardapio(request):
    categorias = Categoria.objects.all()
    lista = []
    for categoria in categorias:
        produtos = Produto.objects.filter(categoria=categoria)
        lista.append([categoria, produtos])
    try:
        estabelecimento = Estabelecimento.objects.all()[0]
    except:
        estabelecimento = Estabelecimento.objects.create(nome='OnShop')

    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
        quantidade = pedido.quantidade_itens
        total = pedido.total
    except:
        quantidade = 0
        total = 0.00

    fuso_local = pytz.timezone('America/Sao_Paulo')
    hora_acesso = datetime.now(fuso_local).time()
    if estabelecimento.horario_abertura < estabelecimento.horario_fechamento: #Significa que abre e fecha no mesmo dia
        if hora_acesso > estabelecimento.horario_abertura and hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    else: #Significa que abre e fecha no dia seguinte
        if hora_acesso > estabelecimento.horario_abertura or hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    estabelecimento.save()

    return render(request, 'onshop_core/cardapio.html', {'lista':lista, 'estabelecimento':estabelecimento, 'quantidade': quantidade, 'total': total})

def ver_carrinho(request):
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
    except:
        pedido = None

    estabelecimento = Estabelecimento.objects.all()[0]

    return render(request, 'onshop_core/carrinho.html', {'pedido':pedido, 'estabelecimento': estabelecimento})

def entregaretirada(request):
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_core:cardapio_inicial') #Se não possui pedido então não é para definir endereço de entrega ainda

    if pedido.quantidade_itens: #Mesmo que haja uma sessão aberta, mas ainda não colocou nada no pedido, também não vai para a definição de entrega
        estabelecimento = Estabelecimento.objects.all()[0]

        local_form = LocalRetiradaPedidoForm()

        return render(request, 'onshop_core/retirada_entrega.html', {'estabelecimento':estabelecimento, 'pedido': pedido, 'form': local_form})
    else:
        return redirect('onshop_core:cardapio_inicial') #Se não possui pedido então não é para definir endereço de entrega ainda

def retirada(request): #View intermediária para setar a escolha de retirada local
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_core:cardapio_inicial')

    if pedido.retirada: #Retira o LocalRetiradaPedido e o sistema entende que por padrão foi escolhido a retirada
        retirada = pedido.retirada
        retirada.pedido_set.clear() #Desacopla o objeto LocalRetiradaPedido do Pedido
        retirada.delete()

    return redirect('onshop_core:contato')

def contato(request):
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_core:cardapio_inicial') #Se não possui pedido, volta para o cardápio

    if pedido.comprador:
        aux = pedido.comprador
    else:
        aux = None

    #Essa função não possui controle da etapa anterior, pois uma vez o campo de retirada não existindo, entende-se que é retirada
    if request.method == 'POST':
        if aux:
            contato = contato_form = ContatoForm(request.POST, instance=aux)
        else:
            contato = contato_form = ContatoForm(request.POST)

        if contato_form.is_valid():
            #contato.save()
            #TODO: Enviar Mensagem
            nome = contato_form.cleaned_data['nome']
            sobrenome = contato_form.cleaned_data['sobrenome']
            telefone = contato_form.cleaned_data['telefone']
            email = contato_form.cleaned_data['email']
            #TODO: Encaminhar para o email do comprador
            if pedido.comprador:
                pedido.comprador.nome = nome
                pedido.comprador.sobrenome = sobrenome
                pedido.comprador.telefone = telefone
                pedido.comprador.email = email
                pedido.comprador.save()
            else:
                comprador = CompradorPedido.objects.create(nome=nome, sobrenome=sobrenome, telefone=telefone, email=email)
                pedido.comprador = 	comprador
            pedido.save()

            return redirect('onshop_core:pagamento')

    else:
        if aux:
            contato_form = ContatoForm(instance=aux)
        else:
            contato_form = ContatoForm()


    return render(request, 'onshop_core/contato.html', {'form': contato_form})

def pagamento(request):
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_core:cardapio_inicial') #Se não possui pedido, volta para o cardápio

    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
        total = pedido.total
    except:
        total = 0.00

    if not pedido.comprador: #Se não possui comprador ainda, deve voltar uma etapa
        return redirect('onshop_core:contato')

    estabelecimento = Estabelecimento.objects.all()[0]
    observacao = estabelecimento.observacao

    return render(request, 'onshop_core/pagamento.html', {'total': total, 'observacao':observacao})

def confirmacao(request):
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
    except:
        return redirect('onshop_core:cardapio_inicial') #Se não possui pedido, volta para o cardápio

    if not pedido.opcao_pagamento:
        return redirect('onshop_core:pagamento')

    estabelecimento = Estabelecimento.objects.all()[0]

    return render(request, 'onshop_core/confirmacao.html', { 'pedido':pedido, 'estabelecimento':estabelecimento })

def remover_pedido(request, pedido_id, produtopedido_id, flag=None):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    produtopedido = get_object_or_404(ProdutoPedido, id=produtopedido_id)

    pedido.produtos.remove(produtopedido)

    pedido.total = pedido.total - produtopedido.total
    pedido.quantidade_itens = pedido.quantidade_itens - produtopedido.quantidade
    pedido.save()

    if flag: #Controle se é remoção vinda do Carrinho vem com flag '1' ou da página de confirmação
        return redirect('onshop_core:ver_carrinho')
    else:
        return redirect('onshop_core:confirmacao')


def concluir_pedido(request):
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
        total = pedido.total
    except:
        return redirect('onshop_core:cardapio_inicial')

    if not pedido.opcao_pagamento:
        return redirect('onshop_core:pagamento')

    verifica_horario()

    estabelecimento = Estabelecimento.objects.all()[0]
    pedido_minimo = estabelecimento.pedido_minimo

    if estabelecimento.status == Estabelecimento.FECHADO:
        return redirect('onshop_core:confirmacao')

    if pedido_minimo and pedido_minimo > total:
        return redirect('onshop_core:confirmacao')
    else:
        pedido.status = Pedido.PEDIDO_NOVO
        pedido.hora_criacao = datetime.now()
        pedido.save()

        enviar_email(pedido.id)
        enviar_notificacao_push(request)

        return render(request, 'onshop_core/pedido_concluido.html', { 'pedido':pedido, 'estabelecimento': estabelecimento })

# ------------ Funções de Acesso -----------
# ------------ -------------------
def painel(request):
    if request.user.is_authenticated():
        pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
        pedidos = pedidos.count()
        push = PushSignal.objects.all()[0]

        return render(request, 'onshop_core/painel_inicial.html', {'pedidos':pedidos, 'app_id': push.app_id})
    else:
        if request.method == 'POST':
            registro = form = AcessarForm(request.POST)
            if form.is_valid():
                usuario = form.acessar()
                password = request.POST['password']
                usuario = authenticate(username=usuario, password=password)
                
                if usuario is not None:
                    login(request, usuario)
                    pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
                    pedidos = pedidos.count()
                    push = PushSignal.objects.all()[0]
                    if request.POST.get('next','onshop_core:administrativo'):
                        return redirect(request.POST.get('next','onshop_core:administrativo'))
                    else:
                        return render(request, 'onshop_core/painel_inicial.html', {'pedidos': pedidos})
                        #return render(request, 'onshop_core/index.html', {})
                else:
                    return render(request, 'onshop_core/acessar.html', {})
        else:
            registro = AcessarForm()
    
        return render(request, 'onshop_core/acessar.html', {'registro': registro})

@login_required
def sair(request):
    if request.user.is_authenticated():
        logout(request)
        
    return redirect('onshop_core:administrativo')

# ------------ Administração de Pedidos -----------
# ------------ -------------------
@login_required
def novos_pedidos(request):
    pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_core/novos_pedidos.html', { 'pedidos':pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados })

@login_required
def pedidos_andamento(request):
    pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos.count()

    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_finalizados = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_core/pedidos_andamento.html', { 'pedidos':pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados })

@login_required
def pedidos_finalizados(request):
    pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos.count()

    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    return render(request, 'onshop_core/pedidos_finalizados.html', { 'pedidos':pedidos, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados})

@login_required
def finalizar_pedido(request, id):
    pedido = get_object_or_404(Pedido, status=Pedido.PEDIDO_ANDAMENTO, id=id)

    pedido.status = Pedido.PEDIDO_FINALIZADO
    pedido.save()

    return redirect('onshop_core:ver_pedido_finalizado' , id=pedido.id)

@login_required
def ver_pedido(request, id):
    try:
        pedido = get_object_or_404(Pedido, status=Pedido.PEDIDO_NOVO, id=id) #Se não for novo está em andamento
    except:
        pedido = get_object_or_404(Pedido, status=Pedido.PEDIDO_ANDAMENTO, id=id)

    if pedido.status == Pedido.PEDIDO_NOVO:
        pedido.status = Pedido.PEDIDO_ANDAMENTO
        pedido.hora_atendimento = datetime.now()
        pedido.save()

    pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos.count()

    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    return render(request, 'onshop_core/ver_pedido.html', { 'pedido':pedido, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados})

@login_required
def ver_pedido_finalizado(request, id):
    pedido = get_object_or_404(Pedido, status=Pedido.PEDIDO_FINALIZADO, id=id)

    pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos.count()

    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    return render(request, 'onshop_core/ver_pedido_finalizado.html', { 'pedido':pedido, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados})


# ------------ Configuração Estebelecimento  -----------
# ------------ -------------------	
@login_required
def config_estabelecimento(request):
    #if id:
    #	auxiliar = get_object_or_404(Estabelecimento, id=id)
    try:
        auxiliar = Estabelecimento.objects.all()[0]
    except:
        auxiliar = False

    if request.method == 'POST':
        if auxiliar:
            estabelecimento = estabelecimento_form = EstabelecimentoForm(request.POST, instance=auxiliar)
        else:
            estabelecimento = estabelecimento_form = EstabelecimentoForm(request.POST)

        if estabelecimento_form.is_valid():
            estabelecimento.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:config_estabelecimento')

    else:
        if auxiliar:
            estabelecimento_form = EstabelecimentoForm(instance=auxiliar)
        else:
            estabelecimento_form = EstabelecimentoForm()

    return render(request, 'onshop_core/preferences.html', {'form':estabelecimento_form })

@login_required
def config_perfil(request):

    if request.method == 'POST':
        perfil = perfil_form = PerfilForm(request.POST, instance=request.user)

        if perfil_form.is_valid():
            password = perfil_form.cleaned_data["password1"]
            if password:
                user = request.user
                user.set_password(password)
                user.save()

            perfil.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:config_perfil')

    else:
        perfil_form = PerfilForm(instance=request.user)

    return render(request, 'onshop_core/perfil.html', {'form': perfil_form})

@login_required
def ver_bairros(request):
    estabelecimento = Estabelecimento.objects.all()[0]

    bairros = BairrosAtendidos.objects.filter(estabelecimento=estabelecimento)

    return render(request, 'onshop_core/bairros.html', {'bairros': bairros, 'estabelecimento': estabelecimento})

@login_required
def adicionar_bairro(request, id=None):
    if id:
        aux = get_object_or_404(BairrosAtendidos, id=id)

    if request.method == 'POST':
        if id:
            bairro = bairro_form = BairroForm(request.POST, instance=aux)
        else:
            bairro = bairro_form = BairroForm(request.POST)

        if bairro_form.is_valid():
            estabelecimento = Estabelecimento.objects.all()[0]
            bairro = bairro_form.save(commit=False)
            bairro.estabelecimento = estabelecimento
            bairro.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_bairros')

    else:
        if id:
            bairro_form = BairroForm(instance=aux)
        else:
            bairro_form = BairroForm()

    return render(request, 'onshop_core/form_bairro.html', {'form': bairro_form})

@login_required
def deletar_bairro(request, id):
    bairro = get_object_or_404(BairrosAtendidos, id=id)

    bairro.delete()

    return redirect('onshop_core:ver_bairros')

@login_required
def config_push(request):
    #if id:
    #	auxiliar = get_object_or_404(Estabelecimento, id=id)
    try:
        auxiliar = PushSignal.objects.all()[0]
    except:
        auxiliar = False

    if request.method == 'POST':
        if auxiliar:
            push = push_form = PushSignalForm(request.POST, instance=auxiliar)
        else:
            push = push_form = PushSignalForm(request.POST)

        if push_form.is_valid():
            push.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:config_push')

    else:
        if auxiliar:
            push_form = PushSignalForm(instance=auxiliar)
        else:
            push_form = PushSignalForm()

    return render(request, 'onshop_core/push.html', {'form':push_form })


# ------------ Produtos -----------
# ------------ -------------------
@login_required
def admin_produtos(request):
    produtos = Produto.objects.all()

    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_core/admin_produtos.html', {'produtos':produtos, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados })

@login_required
def editar_produtos(request, id=None):
    if id:
        auxiliar = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        if id:
            produto = produto_form = ProdutoForm(request.POST, request.FILES, instance=auxiliar)
        else:
            produto = produto_form = ProdutoForm(request.POST, request.FILES)

        if produto_form.is_valid():
            produto = produto_form.save(commit=False)
            produto.save()
            produto_form.save_m2m() #Necessario por conta do Many to Many e do commit False
            #TODO: Enviar Mensagem

            return redirect('onshop_core:admin_produtos')

    else:
        if id:
            produto_form = ProdutoForm(instance=auxiliar)
        else:
            produto_form = ProdutoForm()

    return render(request, 'onshop_core/form_produto.html', {'form': produto_form})

@login_required
def deletar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    produto.delete()
    #TODO: Enviar Mensagem

    return redirect('onshop_core:admin_produtos')

# ------------ Categorias -----------
# ------------ -------------------
@login_required
def ver_categorias(request):
    categorias = Categoria.objects.all()

    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_core/categorias.html', {'categorias':categorias, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados })

@login_required
def editar_categorias(request, id=None):
    if id:
        auxiliar = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        if id:
            categoria = categoria_form = CategoriaForm(request.POST, instance=auxiliar)
        else:
            categoria = categoria_form = CategoriaForm(request.POST)

        if categoria_form.is_valid():
            categoria.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_categorias')
    else:
        if id:
            categoria_form = CategoriaForm(instance=auxiliar)
        else:
            categoria_form = CategoriaForm()

    return render(request, 'onshop_core/form.html', {'form': categoria_form})

@login_required
def deletar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    categoria.delete()
    #TODO: Enviar Mensagem

    return redirect('onshop_core:ver_categorias')

# ------------ Atributos -----------
# ------------ -------------------
@login_required
def ver_atributos(request):
    atributos = Atributo.objects.all()

    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()

    return render(request, 'onshop_core/atributos.html', {'atributos':atributos, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados })

@login_required
def editar_atributos(request, id=None):
    if id:
        auxiliar = get_object_or_404(Atributo, id=id)

    if request.method == 'POST':
        if id:
            atributo = atributo_form = AtributoForm(request.POST, request.FILES, instance=auxiliar)
        else:
            atributo = atributo_form = AtributoForm(request.POST, request.FILES)

        if atributo_form.is_valid():
            atributo = atributo_form.save(commit=False)
            atributo.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_atributos')
    else:
        if id:
            atributo_form = AtributoForm(instance=auxiliar)
        else:
            atributo_form = AtributoForm()

    return render(request, 'onshop_core/form_atributo.html', {'form': atributo_form})

@login_required
def deletar_atributos(request, id):
    atributo = get_object_or_404(Atributo, id=id)

    atributo.delete()
    #TODO: Enviar Mensagem

    return redirect('onshop_core:ver_atributos')

# ------------ Complementos -----------
# ------------ -------------------
@login_required
def adicionar_complemento(request, id):
    produto = get_object_or_404(Produto, id=id)
    perguntas = Pergunta.objects.filter(produto=produto)

    return render(request, 'onshop_core/complementos.html', {'produto':produto, 'perguntas': perguntas})

@login_required
def adicionar_pergunta(request, id, id_pergunta=None):
    produto = get_object_or_404(Produto, id=id)

    if id_pergunta:
        auxiliar = get_object_or_404(Pergunta, id=id_pergunta)

    if request.method == 'POST':
        if id_pergunta:
            pergunta = pergunta_form = PerguntaForm(request.POST, request.FILES, instance=auxiliar)
        else:
            pergunta = pergunta_form = PerguntaForm(request.POST, request.FILES)

        if pergunta_form.is_valid():
            pergunta = pergunta_form.save(commit=False)
            pergunta.produto = produto
            pergunta.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:adicionar_complemento', id=produto.id)
    else:
        if id_pergunta:
            pergunta_form = PerguntaForm(instance=auxiliar)
        else:
            pergunta_form = PerguntaForm()

    return render(request, 'onshop_core/perguntas.html', {'produto':produto, 'form': pergunta_form})

@login_required
def ver_respostas(request, id_pergunta):
    pergunta = get_object_or_404(Pergunta, id=id_pergunta)
    produto = pergunta.produto
    respostas = Resposta.objects.filter(pergunta=pergunta)

    return render(request, 'onshop_core/respostas.html', {'produto':produto, 'pergunta': pergunta, 'respostas': respostas})

@login_required
def adicionar_resposta(request, id_pergunta, id_resposta=None):
    pergunta = get_object_or_404(Pergunta, id=id_pergunta)
    produto = pergunta.produto

    if id_resposta:
        auxiliar = get_object_or_404(Resposta, id=id_resposta)

    if request.method == 'POST':
        if id_resposta:
            resposta = resposta_form = RespostaForm(request.POST, request.FILES, instance=auxiliar)
        else:
            resposta = resposta_form = RespostaForm(request.POST, request.FILES)

        if resposta_form.is_valid():
            resposta = resposta_form.save(commit=False)
            resposta.pergunta = pergunta
            resposta.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_respostas', id_pergunta=pergunta.id)
    else:
        if id_resposta:
            resposta_form = RespostaForm(instance=auxiliar)
        else:
            resposta_form = RespostaForm()

    return render(request, 'onshop_core/form_resposta.html', {'produto':produto, 'pergunta': pergunta, 'form': resposta_form})

@login_required
def deletar_pergunta(request, id_pergunta):
    '''
    Deleta também as respostas
    '''
    pergunta = get_object_or_404(Pergunta, id=id_pergunta)
    produto = pergunta.produto
    respostas = Resposta.objects.filter(pergunta=pergunta)

    for resposta in respostas:
        resposta.delete()

    pergunta.delete()

    #TODO: Enviar Mensagem

    return redirect('onshop_core:adicionar_complemento', id=produto.id)

@login_required
def deletar_resposta(request, id_resposta):
    resposta = get_object_or_404(Resposta, id=id_resposta)
    pergunta = resposta.pergunta

    resposta.delete()

    #TODO: Enviar Mensagem

    return redirect('onshop_core:ver_respostas', id_pergunta=pergunta.id)
# ------------ Complementos Modelo -----------
# ------------ -------------------
@login_required
def ver_complementos(request):
    complementos = ComplementoModelo.objects.all()
    '''
    pedidos_novos = Pedido.objects.filter(status=Pedido.PEDIDO_NOVO)
    qtde_novos_pedidos = pedidos_novos.count()

    pedidos_andamento = Pedido.objects.filter(status=Pedido.PEDIDO_ANDAMENTO)
    qtde_pedidos_andamento = pedidos_andamento.count()

    pedidos_finalizados = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    qtde_pedidos_finalizados = pedidos_finalizados.count()
    
    return render(request, 'onshop_auto/lista_complementos_modelo.html', {'complementos':complementos, 'qtde_novos_pedidos': qtde_novos_pedidos, 'qtde_pedidos_andamento': qtde_pedidos_andamento, 'qtde_pedidos_finalizados': qtde_pedidos_finalizados })
    '''
    return render(request, 'onshop_core/lista_complementos_modelo.html', {'complementos':complementos })

@login_required
def ver_lista_complemento(request, id=id):
    complemento_modelo = get_object_or_404(ComplementoModelo, id=id)
    perguntas_modelo = PerguntaModelo.objects.filter(modelo=complemento_modelo)

    return render(request, 'onshop_core/ver_lista_complementos_modelo.html', {'complemento':complemento_modelo, 'perguntas':perguntas_modelo})

@login_required
def editar_complementos(request, id=None):
    if id:
        auxiliar = get_object_or_404(ComplementoModelo, id=id)

    if request.method == 'POST':
        if id:
            modelo = modelo_form = ComplementoModeloForm(request.POST, request.FILES, instance=auxiliar)
        else:
            modelo = modelo_form = ComplementoModeloForm(request.POST, request.FILES)

        if modelo_form.is_valid():
            modelo = modelo_form.save(commit=False)
            modelo.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_lista_complemento', id=modelo.id)
    else:
        if id:
            modelo_form = ComplementoModeloForm(instance=auxiliar)
        else:
            modelo_form = ComplementoModeloForm()

    return render(request, 'onshop_core/editar_complementos_modelo.html', {'form': modelo_form})

@login_required
def adicionar_pergunta_modelo(request, id, id_pergunta=None):
    modelo = get_object_or_404(ComplementoModelo, id=id)

    if id_pergunta:
        auxiliar = get_object_or_404(PerguntaModelo, id=id_pergunta)

    if request.method == 'POST':
        if id_pergunta:
            pergunta = pergunta_form = PerguntaModeloForm(request.POST, request.FILES, instance=auxiliar)
        else:
            pergunta = pergunta_form = PerguntaModeloForm(request.POST, request.FILES)

        if pergunta_form.is_valid():
            pergunta = pergunta_form.save(commit=False)
            pergunta.modelo = modelo
            pergunta.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_lista_complemento', id=modelo.id)
    else:
        if id_pergunta:
            pergunta_form = PerguntaModeloForm(instance=auxiliar)
        else:
            pergunta_form = PerguntaModeloForm()

    return render(request, 'onshop_core/perguntas_modelo.html', {'complemento': modelo, 'modelo':modelo, 'form': pergunta_form})#Só para poder pegar a url de quem ele herda

@login_required
def deletar_complemento_modelo(request, id=None):
    '''
    Deleta Perguntas e Respostas Modelo
    '''
    modelo = get_object_or_404(ComplementoModelo, id=id)

    perguntas = PerguntaModelo.objects.filter(modelo=modelo)

    for pergunta in perguntas:
        deletar_pergunta_modelo(id_pergunta=pergunta.id)

    modelo.delete()

    return redirect('onshop_core:ver_complementos')

@login_required
def deletar_pergunta_modelo(request, id_pergunta):
    '''
    Deleta também as respostas
    '''
    pergunta = get_object_or_404(PerguntaModelo, id=id_pergunta)
    modelo = pergunta.modelo
    respostas = RespostaModelo.objects.filter(pergunta=pergunta)

    for resposta in respostas:
        resposta.delete()

    pergunta.delete()

    #TODO: Enviar Mensagem

    return redirect('onshop_core:ver_lista_complemento', id=modelo.id)

@login_required
def ver_respostas_modelo(request, id_pergunta):
    pergunta = get_object_or_404(PerguntaModelo, id=id_pergunta)
    modelo = pergunta.modelo
    respostas = RespostaModelo.objects.filter(pergunta=pergunta)

    return render(request, 'onshop_core/respostas_modelo.html', {'complemento':modelo, 'modelo':modelo, 'pergunta': pergunta, 'respostas': respostas})

@login_required
def adicionar_resposta_modelo(request, id_pergunta, id_resposta=None):
    pergunta = get_object_or_404(PerguntaModelo, id=id_pergunta)
    modelo = pergunta.modelo

    if id_resposta:
        auxiliar = get_object_or_404(RespostaModelo, id=id_resposta)

    if request.method == 'POST':
        if id_resposta:
            resposta = resposta_form = RespostaModeloForm(request.POST, request.FILES, instance=auxiliar)
        else:
            resposta = resposta_form = RespostaModeloForm(request.POST, request.FILES)

        if resposta_form.is_valid():
            resposta = resposta_form.save(commit=False)
            resposta.pergunta = pergunta
            resposta.save()
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_respostas_modelo', id_pergunta=pergunta.id)
    else:
        if id_resposta:
            resposta_form = RespostaModeloForm(instance=auxiliar)
        else:
            resposta_form = RespostaModeloForm()

    return render(request, 'onshop_core/form_resposta_modelo.html', {'complemento':modelo,'modelo':modelo, 'pergunta': pergunta, 'form': resposta_form})

@login_required
def deletar_resposta_modelo(request, id_resposta):
    resposta = get_object_or_404(RespostaModelo, id=id_resposta)

    pergunta = resposta.pergunta

    resposta.delete()

    return redirect('onshop_core:ver_respostas_modelo', id_pergunta=pergunta.id)

@login_required
def atribuir_produtos(request, complemento_id):
    '''
    Substitui as perguntas existentes pelas do Modelo
    '''
    complemento = get_object_or_404(ComplementoModelo, id=complemento_id)
    perguntas_modelo = PerguntaModelo.objects.filter(modelo=complemento)

    if request.method == 'POST':
        produtos = atribuir_form = AtribuirForm(request.POST, request.FILES)

        if atribuir_form.is_valid():
            #atribuidos = request.POST.getlist('produtos') #Pega todos os values dos produtos setados
            atribuidos = atribuir_form.cleaned_data['produtos']

            for x in atribuidos:
                produto = get_object_or_404(Produto, id=x)
                perguntas = Pergunta.objects.filter(produto=produto)
                # Faz a deleção das perguntas e respostas existentes
                for pergunta in perguntas:
                    deletar_pergunta(request, pergunta.id)
                # Faz a substituição pelas perguntas e respostas do modelo
                for pergunta in perguntas_modelo:
                    pergunta_atribuida = Pergunta.objects.create(produto=produto, pergunta=pergunta.pergunta, tipo=pergunta.tipo, limite=pergunta.limite)
                    respostas_modelo = RespostaModelo.objects.filter(pergunta=pergunta)
                    for resposta in respostas_modelo:
                        resposta_atribuida = Resposta.objects.create(pergunta=pergunta_atribuida, resposta=resposta, preco_adicional=resposta.preco_adicional)
            #Faz a atribuição
            #TODO: Enviar Mensagem

            return redirect('onshop_core:ver_lista_complemento', id=complemento.id)

    else:
        atribuir_form = AtribuirForm()

    return render(request, 'onshop_core/atribuir_form.html', {'complemento':complemento, 'perguntas':perguntas_modelo, 'form': atribuir_form})

# ------------ Relatório -----------
# ------------ -------------------
@login_required
def relatorio(request):
    #Fazer um deltatime com a hora e data inicial do dia
    '''
    relatorios = Relatorio.objects.filter(data__ge=datetime.date.now())#Pega os últimos sete relatórios

    pedidos_hoje = Pedido.objects.filter(hora_criacao=datetime.date.now())#Pega os pedidos que foram de hoje

    quantidade_pedidos = pedidos_hoje.count()
    valor_total = 0.0

    for pedido in pedidos_hoje: #Pega o valor do total dos pedidos feito hoje
        valor_total = valor_total + pedido.total
    '''
    relatorios = None
    valor_total = 0.0
    quantidade_pedidos = None

    return render(request, 'onshop_core/relatorio.html', {'quantidade_pedidos':quantidade_pedidos, 'valor_total':valor_total, 'relatorios': relatorio})

# ------------ Impressão -----------
# ------------ -------------------

import io as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    #context = Context(context_dict)
    html  = template.render(context_dict)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result) #ISO-8859-1
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


@login_required
def imprimir_pedido(request):

    return render_to_pdf('onshop_core/pedido.html',
            {
                'pagesize':'A4',
            }
        )


@login_required
def imprimir_comanda(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    estabelecimento = Estabelecimento.objects.all()[0]
    estabelecimento = estabelecimento.nome

    return render_to_pdf('onshop_core/pedido.html',
            {
                'pagesize':'A4',
                'pedido': pedido,
                'estabelecimento': estabelecimento,
            }
        )

@login_required
def imprimir_comanda_alternativa(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    estabelecimento = Estabelecimento.objects.all()[0]
    estabelecimento = estabelecimento.nome

    return render(request, 'onshop_core/pedido_alternativo.html', {'estabelecimento':estabelecimento, 'pedido':pedido})

# ------------ Ajax Mobile (Cliente Final) -----------
# ------------ -------------------

#
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
#class ProdutoMobile(View):
#	def get(self, request, id):
#		produto = get_object_or_404(Produto, id=id)
#		data = dict()
#		data['produto'] = model_to_dict(produto)

#		return render(request, 'onshop_core/produto_mobile.html', {'data': data})

        #return render(request, get_template('accounts', request.is_ajax()))*/


def ver_produto_mobile(request):
    id_produto = request.GET.get('id', None)
    produto = get_object_or_404(Produto, id=id_produto)
    perguntas = Pergunta.objects.filter(produto=produto)
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

    rendered = render_to_string('onshop_core/produto_mobile.html', context)

    return JsonResponse({'product_snippet':rendered})

from django.views.decorators.csrf import csrf_exempt
import json

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
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO) #Se existe um pedido em outro estado com essa mesma sessão, considera-se um novo pedido a ser realizado
    except:
        request.session.create() #Cria uma nova sessão
        pedido = Pedido.objects.create(session_key=request.session.session_key)



    nome, quantidade_pp = lista_respostas[-1]
    adicional_pp = Decimal(0) #Calculado através da lista de complementos
    total_pp = Decimal(0) #Calculado através da lista de complementos
    produto = get_object_or_404(Produto, id=id_produto)

    lista_complemento = []
    for x,y in lista_respostas:
        if x.startswith('especial'): # Campo do pedido especial
            if y:
                lista_complemento.append(['\nPEDIDO ESPECIAL', y])
            break
        if x.startswith('quantity'): # Campo do pedido quantidade
            # Faz os cálculos finais do Pedido
            # Não precisa ser feito nada, uma vez que já se pega a quantidade pela lista_respostas
            break

        if x.startswith('question_'):
            resposta = get_object_or_404(Resposta, id=y) #Objeto Resposta está no value
            lista_complemento.append(['\n' + resposta.pergunta.pergunta, resposta.resposta])

            if resposta.preco_adicional: # A lista de respostas para múltipla e exclusiva só são recebidas quando são respondidas
                #Acrescenta no Pedido
                adicional_pp = adicional_pp + resposta.preco_adicional

        else: #Se não é pergunta de escolha e nem especial é Resposta Recorrente
            resposta = get_object_or_404(Resposta, id=x) #Objeto Resposta está no name

            if y != "0":
                complemento = resposta.pergunta.pergunta + ' ' + resposta.resposta
                lista_complemento.append([complemento, y])
                if resposta.preco_adicional:
                    #Acrescenta no Pedido vezes a quantidade do value
                    adicional_pp = adicional_pp + int(y)*resposta.preco_adicional
                    pass


    if produto.preco_promocao:
        total_pp = int(quantidade_pp)*produto.preco_promocao + int(quantidade_pp)*adicional_pp
        preco_pp = produto.preco_promocao
    else:
        total_pp = int(quantidade_pp)*produto.preco + int(quantidade_pp)*adicional_pp
        preco_pp = produto.preco

    produtopedido = ProdutoPedido.objects.create(produto=produto, quantidade=quantidade_pp, preco_produto=preco_pp, adicional=adicional_pp, total=total_pp)
    lista_aux = []
    for i in lista_complemento:
        lista_aux.append(': '.join(i))

    produtopedido.complemento = '<br/>'.join(lista_aux)
    produtopedido.save()

    session_key = pedido.session_key
    #Atualizando o Pedido Geral
    pedido.produtos.add(produtopedido)
    pedido.total = Decimal(pedido.total) + Decimal(total_pp)
    pedido.quantidade_itens = pedido.quantidade_itens + int(quantidade_pp)
    pedido.save()
    '''
    
    pedido.quantidade_itens = pedido.quantidade_itens + quantidade_pp
    pedido.save()
    '''
    #produto_pedido = ProdutoPedido.objects.create(produto=produto)
    #Pega as informações complementares
    #Pega o valor de quantidade
    #Faz o cálculo do pedido
    #Insere no Pedido do Carrinho

    return JsonResponse({'status': 'ok', 'quantidade': pedido.quantidade_itens, 'total': pedido.total })
    #return JsonResponse({'status': 'ok', 'produto': id_produto, 'formData': form_data, 'lista': lista_respostas, 'session_key': session_key, 'key': key, 'lista_complemento': lista_complemento, 'quantidade': pedido.quantidade_itens, 'total': pedido.total })


@csrf_exempt
def analisa_pedido(request):
    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
        total = pedido.total
    except:
        response = JsonResponse({'status': 'error', 'product_snippet': 'Não é possível fazer o pedido nesse momento!'})
        response.status_code = 404
        return response

    verifica_horario()

    estabelecimento = Estabelecimento.objects.all()[0]
    pedido_minimo = estabelecimento.pedido_minimo

    if estabelecimento.status == Estabelecimento.FECHADO:
        response = JsonResponse({'status': 'error', 'product_snippet': 'O estabelecimento se encontra fechado nesse momento!'})
        response.status_code = 404
        return response

    if pedido_minimo and pedido_minimo > total:
        snippet = 'Pedido Mínimo de R$ ' + str(pedido_minimo)
        response = JsonResponse({'status':'error', 'product_snippet': snippet})
        response.status_code = 404
        return response
    else:
        p_etapa = reverse('onshop_core:entregaretirada')
        return JsonResponse({'status':'ok', 'product_snippet': p_etapa })

    return JsonResponse({'status':'ok', 'product_snippet': '' })

def ver_entrega_pedido(request):
    id_pedido = request.GET.get('id', None)
    bairro = request.GET.get('bairro', None)
    cidade = request.GET.get('cidade', None)
    endereco = request.GET.get('endereco', None)

    #return JsonResponse({'status': 'ok', 'id_pedido': endereco, 'product_snippet': 'Endereço registrado com sucesso!'})

    estabelecimento = Estabelecimento.objects.all()[0]

    bairros_atendidos = BairrosAtendidos.objects.filter(estabelecimento=estabelecimento)
    lista_bairros = []
    for i in bairros_atendidos:
        lista_bairros.append(i.bairro)

    if bairro in lista_bairros:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'nope', 'product_snippet': 'Endereço indisponível para entrega!'})

    #return JsonResponse({'status': 'ok', 'product_snippet': 'Esse endereço não é atendido pelo estabelceimento!'})

def receber_endereco(request):
    if request.is_ajax():
        id_pedido = request.GET.get('id', None)

        form_data = request.GET.get('formData', None)

        data = json.loads(form_data)

        #endereco = data["endereco"]
        pedido = get_object_or_404(Pedido, id=id_pedido)


        lista_respostas = []
        for dic in data:
            lista_respostas.append(dic.values())

        endereco = numero = ed_apto_bloco = pto_referencia = ''

        for x,y in lista_respostas:
            if x == 'endereco':
                endereco = y
            if x == 'numero':
                numero = y
            if x == 'ed_apto_bloco':
                ed_apto_bloco = y
            if x == 'pto_referencia':
                pto_referencia = y


        if pedido.retirada:
            pedido.retirada.endereco = endereco
            pedido.retirada.numero = numero
            pedido.retirada.ed_apto_bloco = ed_apto_bloco
            pedido.retirada.pto_referencia = pto_referencia
            pedido.retirada.save()
        else:
            retirada = LocalRetiradaPedido.objects.create(endereco=endereco, numero=numero, ed_apto_bloco=ed_apto_bloco, pto_referencia=pto_referencia)
            pedido.retirada = retirada
        pedido.save()

        return JsonResponse({'status': 'ok', 'form_data': form_data, 'lista_respostas': lista_respostas})
    else:
        return JsonResponse({'status': 'ok'})

@csrf_exempt
def setar_pagamento(request, opcao):#Recebe se cartão ou dinheiro
    pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)

    lista_respostas = []
    if opcao == 'dinheiro':
        form_data = request.GET.get('formData', None)

        data = json.loads(form_data)

        #pedido = get_object_or_404(Pedido, id=id_pedido)

        lista_respostas = []
        for dic in data:
            lista_respostas.append(dic.values())

        for x,y in lista_respostas:
            if x == 'troco_field':
                troco = y

        if pedido.opcao_pagamento:
            pedido.opcao_pagamento.forma = 'Dinheiro'
            pedido.opcao_pagamento.troco = troco
            pedido.opcao_pagamento.save()
        else:
            opcao_pagamento = OpcaoPagamento.objects.create(forma='Dinheiro', troco=troco)
            pedido.opcao_pagamento = opcao_pagamento
        pedido.save()

    if opcao == 'cartao':

        if pedido.opcao_pagamento:
            pedido.opcao_pagamento.forma = 'Cartão'
            pedido.opcao_pagamento.troco = ''
            pedido.opcao_pagamento.save()
        else:
            opcao_pagamento = OpcaoPagamento.objects.create(forma='Cartão')
            pedido.opcao_pagamento = opcao_pagamento

        pedido.save()

    return JsonResponse({'status': 'ok'})

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
def api(request):
    pedidos = Pedido.objects.filter(status=Pedido.PEDIDO_FINALIZADO)
    lista_pedidos = []

    for pedido in pedidos:
        lista_produtos = []
        produtos = pedido.produtos.all()
        '''
        for produto in produtos:
            lista_produtos.append([produto])
        '''
        lista_comprador = [pedido.comprador.nome, pedido.comprador.sobrenome, pedido.comprador.telefone]
        lista_pedidos.append([pedido.id, pedido.hora_atendimento, pedido.quantidade_itens, pedido.total, lista_comprador, lista_produtos])

    pedidos = json.dumps(lista_pedidos, cls=DjangoJSONEncoder)

    return HttpResponse(pedidos)

# ------------ Envios de Email -----------
# ------------ -------------------
from django.core.mail import send_mail

def enviar_email(id):#Função que envia email para o comprador do Pedido
    pedido = get_object_or_404(Pedido, id=id)
    estabelecimento = Estabelecimento.objects.all()[0]
    comprador = pedido.comprador
    email = comprador.email
    nome = comprador.nome
    sobrenome = comprador.sobrenome
    
    #Contexto para o Email     
    c = {
        'pedido': pedido,
        'estabelecimento': estabelecimento,
    }
    message = render_to_string('onshop_core/email_pedido.html', c)
    
    #Enviando mensagem para a pessoa que foi cadastrada
    send_mail('['+ estabelecimento.nome + '] Obrigado pelo seu Pedido! :) ', message, 'onshop.sistema@gmail.com', [email])

    return True

# ------------ Envio Notificação Push -----------
# ------------ -------------------
import requests # pip install requests
import json

def enviar_notificacao_push(request):

    auxiliar = PushSignal.objects.all()[0]
    authorization = auxiliar.authorization
    app_id = auxiliar.app_id

    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic " + authorization }

    payload = {"app_id": app_id,
            "included_segments": ["All"],
            "url": "http://" + request.META['HTTP_HOST'] + "/on/painel/novos-pedidos/",
            "headings": {"en": "Novo pedido chegando", "pt": "Novo pedido chegando"},
            "contents": {"en": "Foi realizado um novo pedido!", "pt": "Foi realizado um novo pedido!"}}

    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
 
    #print(req.status_code, req.reason)
    return True

def verifica_horario():

    try:
        estabelecimento = Estabelecimento.objects.all()[0]
    except:
        estabelecimento = Estabelecimento.objects.create(nome='OnShop')

    try:
        pedido = get_object_or_404(Pedido, session_key=request.session.session_key, status=Pedido.PEDIDO_CARRINHO)
        quantidade = pedido.quantidade_itens
        total = pedido.total
    except:
        quantidade = 0
        total = 0.00

    fuso_local = pytz.timezone('America/Sao_Paulo')
    hora_acesso = datetime.now(fuso_local).time()
    if estabelecimento.horario_abertura < estabelecimento.horario_fechamento: #Significa que abre e fecha no mesmo dia
        if hora_acesso > estabelecimento.horario_abertura and hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    else: #Significa que abre e fecha no dia seguinte
        if hora_acesso > estabelecimento.horario_abertura or hora_acesso < estabelecimento.horario_fechamento:
            estabelecimento.status = Estabelecimento.ABERTO
        else:
            estabelecimento.status = Estabelecimento.FECHADO
    estabelecimento.save()

    return True