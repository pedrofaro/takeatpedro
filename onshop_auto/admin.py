# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CategoriaAuto, AtributoAuto, ProdutoAuto, Codigo, Mesa, Comanda, ComandaSession, CompradorPedidoAuto, MensagemAuto, ItemPedidoAuto, PedidoAuto, Avaliacao

# Register your models here.
admin.site.register(ProdutoAuto)
admin.site.register(Codigo)
admin.site.register(Mesa)
admin.site.register(Comanda)
admin.site.register(ComandaSession)
admin.site.register(CompradorPedidoAuto)
admin.site.register(MensagemAuto)
admin.site.register(ItemPedidoAuto)
admin.site.register(PedidoAuto)
admin.site.register(Avaliacao)