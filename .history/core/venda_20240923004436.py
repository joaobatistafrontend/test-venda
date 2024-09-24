from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.generic import TemplateView,CreateView,View,ListView,UpdateView,DeleteView
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from urllib.parse import urlencode
from django.http import HttpRequest
from django.db.models import Q



class VendaView(TemplateView):
    template_name = 'venda.html'

    def get(self, request):
        produtos = Produto.objects.all()
        carinho = Carrinho.objects.all()
        return render(request, self.template_name, {'produtos':produtos, 'carinho':carinho})
    def post(self, request):
        produto_id = request.POST.get('produto_id')
        if '' in request.POST:
            produto = Produto.objects.get(id=produto_id)
            item_carrinho, created = Carrinho.objects.get_or_create(produto=produto)
            if not created:
                item_carrinho.quantidade += 1
            item_carrinho.save()
            if item:
            print(f"Produto adicionado: {produto.nome_produto}, Quantidade no carrinho: {item_carrinho.quantidade}")

        elif 'finalizar_venda' in request.POST:
            carrinho = Carrinho.objects.filter()
            if carrinho.exists():
                venda = Venda.objects.create()
                for item in carrinho:
                    VendaDoProduto.objects.create(
                        venda=venda,
                        produto=item.produto,
                        qtd=item.quantidade,
                        total=item.produto.valor * item.quantidade
                    )
                carrinho.delete()  # Limpa o carrinho após finalizar a venda
            return redirect('venda')

        return redirect('venda')
