from django.contrib import admin
from .models import *

admin.site.register(NovaCategoria)
admin.site.register(Produto)
admin.site.register(ItemDoCarrinho)
admin.site.register(VendaDoProduto)
admin.site.register(Carrinho)
admin.site.register(Venda)