# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import path
from django.conf import settings
from . import views

app_name = 'onshop_core'

urlpatterns = [
    url(r'p_mesas/$', views.p_mesas, name='p_mesas'), #Forma de Pagamento
    url(r'p_painel/$', views.p_painel, name='p_painel'), #Forma de Pagamento
    url(r'forma_pag/$', views.forma_pag, name='forma_pag'), #Forma de Pagamento
    url(r'p_produtos/$', views.p_produtos, name='p_produtos'), #Forma de Pagamento
    url(r'p_pedidos_pag/$', views.p_pedidos_pag, name='p_pedidos_pag'), #Forma de Pagamento
    url(r'^$', views.cardapio, name='cardapio_inicial'), #Página de Cardápio inicial
    url(r'p-etapa/$', views.entregaretirada, name='entregaretirada'), #Primeira Etapa logo após fazer o pedido
    url(r'p-etapa/retirada/$', views.retirada, name='retirada'), #View intermediária para selecionar a retirada
    url(r'carrinho/$', views.ver_carrinho, name='ver_carrinho'), #Tela com os produtos pedidos
    url(r's-etapa/$', views.contato, name='contato'), #Segunda Etapa logo após fazer o pedido
    url(r't-etapa/$', views.pagamento, name='pagamento'), #Terceira Etapa logo após preencher o contato
    url(r'q-etapa/$', views.confirmacao, name='confirmacao'), #Quarta Etapa logo após optar pela forma de pagamento
    url(r'concluido/$', views.concluir_pedido, name='concluir_pedido'), #Quinta Etapa logo após optar pela confirmação
    url(r'^remover-pedido/(?P<pedido_id>\d+)/(?P<produtopedido_id>\d+)/$', views.remover_pedido, name='remover_pedido'), #View de Deleção de Produto Pedido
    url(r'^remover-pedido/(?P<pedido_id>\d+)/(?P<produtopedido_id>\d+)/(?P<flag>\d+)$', views.remover_pedido, name='remover_pedido_carrinho'), #View de Deleção de Produto Pedido
    url(r'^painel/$', views.painel, name='administrativo'), #Página de Administração do Estabelecimento
    url(r'^painel/produtos/$', views.admin_produtos, name='admin_produtos'), #Página de Administração Produtos
    url(r'^painel/produtos/adicionar/$', views.editar_produtos, name='adicionar_produtos'), #Página de Adição Produtos
    url(r'^painel/produtos/editar/(?P<id>\d+)/$', views.editar_produtos, name='editar_produtos'), #Página de Edição Produtos
    url(r'^painel/produtos/deletar/(?P<id>\d+)/$', views.deletar_produto, name='deletar_produto'), #View de Deleção Produtos
    url(r'^painel/produtos/complemento/(?P<id>\d+)/$', views.adicionar_complemento, name='adicionar_complemento'), #View de Adição de Perguntas do Produto
    url(r'^painel/produtos/complemento/pergunta/(?P<id>\d+)/$', views.adicionar_pergunta, name='adicionar_pergunta'), #Formulário de Adição de Perguntas do Produto
	url(r'^painel/produtos/complemento/ver-respostas/(?P<id_pergunta>\d+)/$', views.ver_respostas, name='ver_respostas'), #Formulário de Adição de Respostas do Produto
    url(r'^painel/produtos/complemento/pergunta/(?P<id>\d+)/(?P<id_pergunta>\d+)$', views.adicionar_pergunta, name='editar_pergunta'), #Formulário de Adição de Perguntas do Produto
	url(r'^painel/produtos/complemento/pergunta/deletar/(?P<id_pergunta>\d+)$', views.deletar_pergunta, name='deletar_pergunta'), #Formulário de Deleção de Perguntas do Produto        
    url(r'^painel/produtos/complemento/resposta/(?P<id_pergunta>\d+)/$', views.adicionar_resposta, name='adicionar_resposta'), #Formulário de Adição de Respostas do Produto
    url(r'^painel/produtos/complemento/resposta/(?P<id_pergunta>\d+)/(?P<id_resposta>\d+)$', views.adicionar_resposta, name='editar_resposta'), #Formulário de Edição de Respostas do Produto
    url(r'^painel/produtos/complemento/resposta/deletar/(?P<id_resposta>\d+)$', views.deletar_resposta, name='deletar_resposta'), #Formulário de Deleção de Respostas do Produto    
    url(r'^painel/categorias/$', views.ver_categorias, name='ver_categorias'), #Página de Administração Categorias
    url(r'^painel/categorias/adicionar/$', views.editar_categorias, name='adicionar_categorias'), #Página de Adição Categorias
    url(r'^painel/categorias/editar/(?P<id>\d+)/$', views.editar_categorias, name='editar_categorias'), #Página de Edição Categorias
    url(r'^painel/categorias/deletar/(?P<id>\d+)/$', views.deletar_categoria, name='deletar_categoria'), #View de Deleção Categorias
    url(r'^painel/atributos/$', views.ver_atributos, name='ver_atributos'), #Página de Administração Atributos
    url(r'^painel/atributos/adicionar/$', views.editar_atributos, name='adicionar_atributos'), #Página de Adição Atributos
    url(r'^painel/atributos/editar/(?P<id>\d+)/$', views.editar_atributos, name='editar_atributos'), #Página de Edição Atributos
    url(r'^painel/atributos/deletar/(?P<id>\d+)/$', views.deletar_atributos, name='deletar_atributos'), #View de Deleção Atributos
    url(r'^painel/complementos/$', views.ver_complementos, name='ver_complementos'), #Página de Administração das Perguntas Complementares
    url(r'^painel/complementos/criar/$', views.editar_complementos, name='criar_complementos'), #Página de Administração das Perguntas Complementares
    url(r'^painel/complementos/editar/(?P<id>\d+)/$', views.editar_complementos, name='editar_complementos'), #Página de Administração das Perguntas Complementares
    url(r'^painel/complementos/(?P<id>\d+)/$', views.ver_lista_complemento, name='ver_lista_complemento'), #View de Listagem de Pergunta Complementar Específica
    url(r'^painel/complementos/deletar/(?P<id>\d+)/$', views.deletar_complemento_modelo, name='deletar_complemento_modelo'), #View de Listagem de Pergunta Complementar Específica
    url(r'^painel/complementos/atribuir/(?P<complemento_id>\d+)/$', views.atribuir_produtos, name='atribuir_produtos'), #Formulário de Atribuição a Produtos    
    url(r'^painel/complementos/pergunta/(?P<id>\d+)/$', views.adicionar_pergunta_modelo, name='adicionar_pergunta_modelo'), #Formulário de Adição de Perguntas do Produto
    url(r'^painel/complementos/pergunta/(?P<id>\d+)/(?P<id_pergunta>\d+)/$', views.adicionar_pergunta_modelo, name='editar_pergunta_modelo'), #Formulário de Adição de Perguntas Modelos
    url(r'^painel/complementos/pergunta/(?P<id_pergunta>\d+)/deletar/$', views.deletar_pergunta_modelo, name='deletar_pergunta_modelo'), #Deletar Pergunta Modelo
    url(r'^painel/complementos/ver-respostas/(?P<id_pergunta>\d+)/$', views.ver_respostas_modelo, name='ver_respostas_modelo'), #Formulário de Adição de Respostas do Modelo
    url(r'^painel/complementos/resposta/(?P<id_pergunta>\d+)/$', views.adicionar_resposta_modelo, name='adicionar_resposta_modelo'), #Formulário de Adição de Respostas Modelos
    url(r'^painel/complementos/resposta/(?P<id_pergunta>\d+)/(?P<id_resposta>\d+)/$', views.adicionar_resposta_modelo, name='editar_resposta_modelo'), #Formulário de Edição de Respostas Modelos
    url(r'^painel/complementos/resposta/deletar/(?P<id_resposta>\d+)/$', views.deletar_resposta_modelo, name='deletar_resposta_modelo'), #View de Deleção de Respostas Modelos
    url(r'^painel/novos-pedidos/$', views.novos_pedidos, name='novos_pedidos'), #View de Novos Pedidos
    url(r'^painel/ver-pedido/(?P<id>\d+)/$', views.ver_pedido, name='ver_pedido'), #View de Pedido
    url(r'^painel/ver-pedido-finalizado/(?P<id>\d+)/$', views.ver_pedido_finalizado, name='ver_pedido_finalizado'), #View de Pedido Finalizado
    url(r'^painel/finalizar-pedido/(?P<id>\d+)/$', views.finalizar_pedido, name='finalizar_pedido'), #View de Finalização de Pedido
    url(r'^painel/pedidos-andamento/$', views.pedidos_andamento, name='pedidos_andamento'), #View de Pedidos em Andamento
    url(r'^painel/pedidos-finalizados/$', views.pedidos_finalizados, name='pedidos_finalizados'), #View de Novos Pedidos    
    url(r'^painel/pedido-imprimir/(?P<id>\d+)/$', views.imprimir_comanda, name='imprimir_comanda'), #Teste para impressão    
    url(r'^painel/imprimir-alternativo/(?P<id>\d+)/$', views.imprimir_comanda_alternativa, name='imprimir_comanda_alternativa'),
    url(r'^painel/relatorios/$', views.relatorio, name='relatorio'),
    url(r'^painel/config/$', views.config_estabelecimento, name='config_estabelecimento'), #Página de Administração do Estabelecimento
	url(r'^painel/perfil/$', views.config_perfil, name='config_perfil'), #Página de Administração do Estabelecimento   
    url(r'^painel/push/$', views.config_push, name='config_push'), #Página de Administração da Notificação PUSH
    url(r'^painel/bairros/$', views.ver_bairros, name='ver_bairros'), #Página de Administração do Estabelecimento
    url(r'^painel/bairros/adicionar/$', views.adicionar_bairro, name='adicionar_bairro'), #Página de Administração do Estabelecimento
    url(r'^painel/bairros/editar/(?P<id>\d+)/$', views.adicionar_bairro, name='editar_bairro'), #Página de Edição do Bairro
    url(r'^painel/bairros/deletar/(?P<id>\d+)/$', views.deletar_bairro, name='deletar_bairro'), #Página de Deleção do Bairro
    url(r'^painel/sair/$', views.sair, name='sair'), #Página de Administração do Estabelecimento
    url(r'^painel/pedidoimpresso/$', views.imprimir_pedido, name='imprimir_pedido'), #Teste para impressão

    url(r'^ver-produto/$', views.ver_produto_mobile, name='ver_produto'), #Página de Apresentação do Produto Cliente Final
    url(r'^adicionar-pedido/$', views.adicionar_pedido, name='adicionar_pedido'), #View de Adição de Pedido a um (Novo) Carrinho
    url(r'^ver-entrega-pedido/$', views.ver_entrega_pedido, name='ver_entrega_pedido'), #Call via ajax para configurar o endereço de entrega
    url(r'^receber-endereco/$', views.receber_endereco, name='receber_endereco'), #Call via ajax para configurar o endereço de entrega
    url(r'^pagamento/(?P<opcao>[-\w]+)/$', views.setar_pagamento, name='setar_pagamento'), #View de Configuração de forma pagamento
    url(r'^api/$', views.api, name='api'), #View de Teste para Futura API
    url(r'^analisa-pedido/$', views.analisa_pedido, name='analisa_pedido'), #Chamada ajax para analisar se pode ser feito o pedido
   ]
  