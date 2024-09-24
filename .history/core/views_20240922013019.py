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

        return render(request, self.template_name, {'produtos':produtos})
    def post(self, request):
        produto_id = request.POST.get('produto_id')
        print(f"Produto ID recebido: {produto_id}")  # Para depuração

        if 'adicionar_produto' in request.POST:
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
            print(f"Item adicionado ao carrinho: {item.produto.nome}, Quantidade: {item.quantidade}")  # Para depuração

            return redirect('index')
        else:
            print("Nenhum produto foi adicionado.")  # Para depuração
            return redirect('index')
