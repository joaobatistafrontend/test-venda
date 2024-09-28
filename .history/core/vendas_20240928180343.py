from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto, ItemDoCarrinho, Venda, VendaDoProduto
from django.utils import timezone
from django.db.models import Max
from django.shortcuts import render, get_object_or_404


class VendasView(TemplateView):
    template_name = 'vendas.html'

    def get(self, request, pk):
        venda = get_object_or_404(Venda, pk=pk)
        produtos = Produto.objects.all()

        return render(request, self.template_name, {'venda': venda})