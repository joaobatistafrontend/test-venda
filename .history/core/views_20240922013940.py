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

class IndexView(TemplateView):
    template_name = 'index.html'
    def get(self, request):
        produtos = Produto.objects.all()
        carinho =  ItemDoCarrinho.objects.all()

        return render(request, self.template_name, {'produtos':produtos, 'carinho': carinho})
    


def adicionar_ao_carrinho(request, produto_id):
    if request.method == 'POST':
        produto = get_object_or_404(Produto, pk=produto_id)

        # Verifica se já existe um item do carrinho para este produto
        item, created = ItemDoCarrinho.objects.get_or_create(produto=produto, defaults={'quantidade': 0})

        # Se o item já existe, incrementa a quantidade
        if not created:
            item.quantidade += 1
        else:
            item.quantidade = 1  # Se o item foi criado agora, inicializa a quantidade como 1

        # Calcula o preço total do item no carrinho com base no valor do produto
        item.preco_total = item.quantidade * produto.valor
        item.save()
        return redirect('index')
    else:
        return redirect('index') 
    
def adicionar_no_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    item, created = ItemDoCarrinho.objects.get_or_create(produto=produto)
    if item.quantidade >0:
        item.quantidade += 1
        item.preco_total = item.quantidade * produto.valor
        item.save()
        return redirect('index')
    else:
        return redirect('index')
def remover_do_carrinho(request, produto_id,empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)
    produto = get_object_or_404(Produto, pk=produto_id, empresa=empresa)
    item, created = ItemDoCarrinho.objects.get_or_create(produto=produto, empresa=empresa)
    if item.quantidade > 1:
        item.quantidade -= 1
        item.preco_total = item.quantidade * produto.valor
        item.save()
        print('adcionado')
        # Adiciona uma mensagem de sucesso que será exibida na página
        messages.success(request, f'{produto.nome_produto} foi adicionado ao seu carrinho.')
        return redirect('ver_carrinho',empresa_slug=empresa.slug)
    else:
        item.delete()
    return redirect('ver_carrinho',empresa_slug=empresa.slug)

# View para remover todos item do carrinho
def remover_todos_do_carrinho(request, item_id, empresa_slug):
    empresa = Empresa.objects.get(slug=empresa_slug)
    item = get_object_or_404(ItemDoCarrinho, pk=item_id, empresa=empresa)
    if item.quantidade:
        item.delete()
    return redirect('ver_carrinho', empresa_slug=empresa.slug)
