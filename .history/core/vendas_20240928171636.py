from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto, ItemDoCarrinho, Venda, VendaDoProduto
from django.utils import timezone
from django.db.models import Max
from django.shortcuts import render, get_object_or_404


class VendasView(TemplateView):
    template_name = 'vendas.html'

    def get(self, request):
        produtos = Produto.objects.all()
        total = sum(item.produto.valor * item.quantidade for item in carrinho)
        vendas = VendaDoProduto.objects.all()


        item = ItemDoCarrinho.objects.all()

        total = sum(item.produto.valor * item.quantidade for item in carrinho)

        return render(request, self.template_name, {'produtos': produtos, 'carrinho': carrinho, 'item' : item, 'vendas' : vendas, 'total' : total,})

        