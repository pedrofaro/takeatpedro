# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from . import views

app_name = 'onshop_auto'

urlpatterns = [
	url(r'^$', views.acessar_autoatendimento, name='acessar_autoatendimento'), #Tela Inicial Autoatendimento Usuário Final
	url(r'^registrar-codigo/$', views.registrar_codigo, name='registrar_codigo'),
	url(r'^erro/$', views.codigo_errado, name='codigo_errado'),
	url(r'^cardapio/(?P<id_comanda>\d+)$', views.ver_cardapio, name='ver_cardapio'),
	url(r'ver-carrinho/$', views.ver_carrinho, name='ver_carrinho'), #Tela com os produtos pedidos
    url(r'carrinho/$', views.formulario_carrinho, name='formulario_carrinho'), #Chamado via Ajax
    url(r'carrinho-garcom/(?P<id_comanda>\d+)/(?P<id_garcom>\d+)/(?P<token>\d+)$', views.formulario_carrinho_garcom, name='formulario_carrinho'), #Chamado via Ajax
	url(r'p-etapa/$', views.contato, name='contato'), #Segunda Etapa logo após fazer o pedido
	url(r's-etapa/$', views.confirmacao, name='confirmacao'), #Terceira Etapa logo após preencher contato
	url(r'concluido/$', views.concluir_pedido, name='concluir_pedido'), #Última Etapa
    url(r'concluido-garcom/(?P<id_comanda>\d+)/(?P<id_garcom>\d+)/(?P<token>\d+)$', views.concluir_pedido_garcom, name='concluir_pedido_garcom'), #Última Etapa
    url(r'codigo/(?P<id_codigo>\d+)$', views.registrar_codigo_fora, name='registrar_codigo_fora'), #Função de registro quando se lê o código QR sem ser pelo sistema

	url(r'^ver-produto/$', views.ver_produto_mobile, name='ver_produto'), #Página de Apresentação do Produto Cliente Final
	url(r'^adicionar-pedido/$', views.adicionar_pedido, name='adicionar_pedido'), #View de Adição de Pedido a um (Novo) Carrinho
    url(r'^remover-pedido/(?P<pedido_id>\d+)/(?P<produtopedido_id>\d+)/$', views.remover_pedido, name='remover_pedido'), #View de Deleção de Produto Pedido
    url(r'^remover-pedido/(?P<pedido_id>\d+)/(?P<produtopedido_id>\d+)/(?P<flag>\d+)$', views.remover_pedido, name='remover_pedido_carrinho'), #View de Deleção de Produto Pedido
    url(r'^rejeitar-pedido/$', views.rejeitar_pedido, name='rejeitar_pedido_vazio'), #View de Rejeição de Pedido
    url(r'^rejeitar-pedido/(?P<pedido_id>\d+)/$', views.rejeitar_pedido, name='rejeitar_pedido'), #View de Rejeição de Pedido
    url(r'^inserir-contato/$', views.inserir_contato, name='inserir_contato'), #View de Inserção de Contato no carrinho via Ajax
    url(r'^ajuda/$', views.formulario_ajuda, name='formulario_ajuda'), #Formulário de Ajuda
    url(r'^ver-conta/$', views.ver_parcial, name='ver_parcial'), #Página com a Parcial
    url(r'^pedir-encerramento/$', views.pedir_encerramento_mesa, name='pedir_encerramento_mesa'), #Página com a Parcial
    url(r'^encerramento/(?P<id_comanda>\d+)$', views.ver_avaliacao_modal, name='ver_avaliacao_modal'), #Página com a Avaliação 
    url(r'^pedir-ajuda/$', views.enviar_pedido_ajuda, name='enviar_pedido_ajuda'), #Página com a Parcial
    url(r'^registrar-codigo-ajax/$', views.registrar_codigo_ajax, name="registrar_codigo_ajax"), #Ajax de registro de código da mesa via leitor de QR CODE

	url(r'^painel/$', views.painel_produtos_auto, name='admin_autoatendimento'), #Painel Administrativo Autoatendimento
    url(r'^painel/produtos/adicionar/$', views.editar_produtos_auto, name='adicionar_produtos_auto'), #Página de Adição Produtos
    url(r'^painel/produtos/editar/(?P<id>\d+)/$', views.editar_produtos_auto, name='editar_produtos_auto'), #Página de Edição Produtos
    url(r'^painel/produtos/deletar/(?P<id>\d+)/$', views.deletar_produto_auto, name='deletar_produto_auto'), #View de Deleção Produtos
	url(r'^painel/novos-pedidos/$', views.novos_pedidos_auto, name='novos_pedidos_auto'), #View de Novos Pedidos
	url(r'^painel/pedidos-andamento/$', views.pedidos_andamento, name='pedidos_andamento'), #View de Pedidos em Andamento
	url(r'^painel/pedidos-finalizados/$', views.pedidos_finalizados, name='pedidos_finalizados'), #View de Novos Pedidos    
	url(r'^painel/ver-pedido/(?P<id>\d+)/$', views.ver_pedido, name='ver_pedido'), #View de Pedido
    url(r'^painel/ver-pedido-finalizado/(?P<id>\d+)/$', views.ver_pedido_finalizado, name='ver_pedido_finalizado'), #View de Pedido Finalizado
    url(r'^painel/finalizar-pedido/(?P<id>\d+)/$', views.finalizar_pedido, name='finalizar_pedido'), #View de Finalização de Pedido
    url(r'^painel/imprimir-pedido/(?P<id>\d+)/$', views.imprimir_pedido_auto, name='imprimir_pedido_auto'),

    url(r'^painel/ver-mensagens/$', views.ver_mensagens, name='ver_mensagens'), #View de Mensagens
    url(r'^painel/mensagem-atendida/(?P<id_mensagem>\d+)/$', views.mensagem_atendida, name='mensagem_atendida'), #MArcando Mensagem como Atendida

    url(r'^painel/ver-comandas/$', views.ver_comandas, name='ver_comandas'),
    url(r'^painel/ver-pedidos-comanda/(?P<id_comanda>\d+)/$', views.ver_pedidos_comanda, name='ver_pedidos_comanda'),
	url(r'^painel/imprimir-cupom/(?P<id_comanda>\d+)/$', views.imprimir_cupom, name='imprimir_cupom'),
    url(r'^painel/imprimir-qrcode/(?P<id_mesa>\d+)/$', views.imprimir_qrcode, name='imprimir_qrcode'),

	url(r'^painel/categorias/$', views.ver_categorias, name='ver_categorias_auto'), #Página de Administração Categorias
	url(r'^painel/categorias/adicionar/$', views.editar_categorias, name='adicionar_categorias_auto'), #Página de Adição Categorias
	url(r'^painel/categorias/editar/(?P<id>\d+)/$', views.editar_categorias, name='editar_categorias_auto'), #Página de Edição Categorias
	url(r'^painel/categorias/deletar/(?P<id>\d+)/$', views.deletar_categoria, name='deletar_categoria_auto'), #View de Deleção Categorias
	url(r'^painel/atributos/$', views.ver_atributos, name='ver_atributos_auto'), #Página de Administração Atributos
    url(r'^painel/atributos/adicionar/$', views.editar_atributos, name='adicionar_atributos_auto'), #Página de Adição Atributos
    url(r'^painel/atributos/editar/(?P<id>\d+)/$', views.editar_atributos, name='editar_atributos_auto'), #Página de Edição Atributos
    url(r'^painel/atributos/deletar/(?P<id>\d+)/$', views.deletar_atributos, name='deletar_atributos_auto'), #View de Deleção Atributos
    url(r'^painel/produtos/complemento/(?P<id>\d+)/$', views.adicionar_complemento, name='adicionar_complemento_auto'), #View de Adição de Perguntas do Produto
    url(r'^painel/produtos/complemento/pergunta/(?P<id>\d+)/$', views.adicionar_pergunta, name='adicionar_pergunta_auto'), #Formulário de Adição de Perguntas do Produto
	url(r'^painel/produtos/complemento/ver-respostas/(?P<id_pergunta>\d+)/$', views.ver_respostas, name='ver_respostas_auto'), #Formulário de Adição de Respostas do Produto
    url(r'^painel/produtos/complemento/pergunta/(?P<id>\d+)/(?P<id_pergunta>\d+)$', views.adicionar_pergunta, name='editar_pergunta_auto'), #Formulário de Adição de Perguntas do Produto
	url(r'^painel/produtos/complemento/pergunta/deletar/(?P<id_pergunta>\d+)$', views.deletar_pergunta, name='deletar_pergunta_auto'), #Formulário de Deleção de Perguntas do Produto        
    url(r'^painel/produtos/complemento/resposta/(?P<id_pergunta>\d+)/$', views.adicionar_resposta, name='adicionar_resposta_auto'), #Formulário de Adição de Respostas do Produto
    url(r'^painel/produtos/complemento/resposta/(?P<id_pergunta>\d+)/(?P<id_resposta>\d+)$', views.adicionar_resposta, name='editar_resposta_auto'), #Formulário de Edição de Respostas do Produto
    url(r'^painel/produtos/complemento/resposta/deletar/(?P<id_resposta>\d+)$', views.deletar_resposta, name='deletar_resposta_auto'), #Formulário de Deleção de Respostas do Produto    
	url(r'^painel/complementos/$', views.ver_complementos, name='ver_complementos_auto'), #Página de Administração das Perguntas Complementares
    url(r'^painel/complementos/criar/$', views.editar_complementos, name='criar_complementos_auto'), #Página de Administração das Perguntas Complementares
    url(r'^painel/complementos/editar/(?P<id>\d+)/$', views.editar_complementos, name='editar_complementos_auto'), #Página de Administração das Perguntas Complementares
    url(r'^painel/complementos/(?P<id>\d+)/$', views.ver_lista_complemento, name='ver_lista_complemento_auto'), #View de Listagem de Pergunta Complementar Específica
    url(r'^painel/complementos/deletar/(?P<id>\d+)/$', views.deletar_complemento_modelo, name='deletar_complemento_modelo_auto'), #View de Listagem de Pergunta Complementar Específica
    url(r'^painel/complementos/atribuir/(?P<complemento_id>\d+)/$', views.atribuir_produtos, name='atribuir_produtos_auto'), #Formulário de Atribuição a Produtos    
    url(r'^painel/complementos/pergunta/(?P<id>\d+)/$', views.adicionar_pergunta_modelo, name='adicionar_pergunta_modelo_auto'), #Formulário de Adição de Perguntas do Produto
    url(r'^painel/complementos/pergunta/(?P<id>\d+)/(?P<id_pergunta>\d+)/$', views.adicionar_pergunta_modelo, name='editar_pergunta_modelo_auto'), #Formulário de Adição de Perguntas Modelos
    url(r'^painel/complementos/pergunta/(?P<id_pergunta>\d+)/deletar/$', views.deletar_pergunta_modelo, name='deletar_pergunta_modelo_auto'), #Deletar Pergunta Modelo
    url(r'^painel/complementos/ver-respostas/(?P<id_pergunta>\d+)/$', views.ver_respostas_modelo, name='ver_respostas_modelo_auto'), #Formulário de Adição de Respostas do Modelo
    url(r'^painel/complementos/resposta/(?P<id_pergunta>\d+)/$', views.adicionar_resposta_modelo, name='adicionar_resposta_modelo_auto'), #Formulário de Adição de Respostas Modelos
    url(r'^painel/complementos/resposta/(?P<id_pergunta>\d+)/(?P<id_resposta>\d+)/$', views.adicionar_resposta_modelo, name='editar_resposta_modelo_auto'), #Formulário de Edição de Respostas Modelos
    url(r'^painel/complementos/resposta/deletar/(?P<id_resposta>\d+)/$', views.deletar_resposta_modelo, name='deletar_resposta_modelo_auto'), #View de Deleção de Respostas Modelos
    url(r'^painel/mesas/$', views.ver_mesas, name='ver_mesas'), #Página de Administração das Mesas
    url(r'^painel/mesas-abertas/$', views.ver_mesas_abertas, name='ver_mesas_abertas'), #Página de Administração das Mesas
    url(r'^painel/detalhes-mesa-aberta/(?P<id_mesa>\d+)/$', views.ver_detalhes_mesa_aberta, name='ver_detalhes_mesa_aberta'), #Página de Detalhamento das Mesas
    url(r'^painel/transferir-item/(?P<id_item>\d+)/$', views.transferir_item_pedido, name='transferir_item_pedido'), #Função de transferência de item para outra Mesa
    url(r'^painel/remover-item/(?P<id_item>\d+)/$', views.remover_item_pedido, name='remover_item_pedido'), #Página de Detalhamento das Mesas
    url(r'^painel/mesas-fechadas/$', views.ver_ultimas_mesas_fechadas, name='ver_ultimas_mesas_fechadas'), #Página de Administração das Mesas
    url(r'^painel/mesas/criar/$', views.editar_mesa, name='criar_mesa'), #Página de Administração das Mesas
    url(r'^painel/transferir-mesa/(?P<id_mesa>\d+)/$', views.transferir_mesa_inteira, name='transferir_mesa_inteira'), #Página de Transferência da Mesa
    url(r'^painel/fechar-mesa/(?P<id_mesa>\d+)/$', views.fechar_mesa, name='fechar_mesa'), #Página de Fechamento de Mesa
    url(r'^painel/mesas/renovar-codigo/(?P<id>\d+)/$', views.renovar_codigo_mesa, name='renovar_codigo'), #Renovação do Código
    url(r'^painel/mesas/deletar/(?P<id>\d+)/$', views.deletar_mesa, name='deletar_mesa'), #Página de Administração das Mesas
    url(r'^painel/ver-avaliacoes/$', views.ver_avaliacoes, name='ver_avaliacoes'), #Página de Administração das Avaliações
    url(r'^receber-avaliacao/$', views.receber_avaliacao, name='receber_avaliacao'), #Chamada Ajax que recebe a Avaliação feita

    url(r'^analisa-pedido-auto/$', views.analisa_pedido_auto, name='analisa_pedido_auto'), #Chamada ajax para analisar se pode ser feito o pedido

    # Garcons
    url(r'^painel/garcons/$', views.ver_garcons, name='ver_garcons_auto'),
    url(r'^painel/garcons/editar/$', views.editar_garcons, name='adicionar_garcons_auto'),
    url(r'^painel/garcons/editar/(?P<id>\d+)/$', views.editar_garcons, name='editar_garcons_auto'),
    url(r'^painel/garcons/deletar/(?P<id>\d+)/$', views.deletar_garcom, name='deletar_garcom_auto'),

    url(r'^atendimento/$', views.atendimento_garcom, name='atendimento_garcom'), #Página de acesso do garçom as mesas
    url(r'^atendimento/sair/(?P<id_garcom>\d+)/(?P<token>\d+)/$', views.sair_garcom, name='sair_garcom'),
    url(r'^atendimento/mesas/(?P<id_garcom>\d+)/(?P<token>\d+)/$', views.atendimento_mesas, name='atendimento_mesas'),
    url(r'^atendimento/mesas/(?P<id_garcom>\d+)/(?P<token>\d+)/(?P<codigo>\d+)/$', views.atendimento_mesas, name='atendimento_ver_mesa'),
    url(r'^cardapio/(?P<id_comanda>\d+)/(?P<id_garcom>\d+)/(?P<token>\d+)/$', views.ver_cardapio_garcom, name='ver_cardapio_garcom'),
]

