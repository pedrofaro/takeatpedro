# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
# Register your models here.
from onshop_core.models import Estabelecimento, Categoria, Atributo, Produto, Pergunta, Resposta, Pedido, ProdutoPedido, CompradorPedido, LocalRetiradaPedido, OpcaoPagamento, BairrosAtendidos, PushSignal, PMesa, PProduto, PFormasPag, PPedidosFormaPag, PPedidos

# Register your models here.
admin.site.register(Estabelecimento)
admin.site.register(Categoria)
admin.site.register(Atributo)
admin.site.register(Produto)
admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(Pedido)
admin.site.register(ProdutoPedido)
admin.site.register(CompradorPedido)
admin.site.register(LocalRetiradaPedido)
admin.site.register(OpcaoPagamento)
admin.site.register(BairrosAtendidos)
admin.site.register(PushSignal)
admin.site.register(PMesa)
admin.site.register(PProduto)
admin.site.register(PPedidos)
admin.site.register(PFormasPag)
admin.site.register(PPedidosFormaPag)