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
def remover_do_carrinho(request, from django.db import models
from django.db.models import Max
from decimal import Decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone


class NovaCategoria(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.nome}'


class Produto(models.Model):
    nome = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_categoria = models.ForeignKey(NovaCategoria, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} x {self.valor}"  


class ItemDoCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    preco_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calcula o preço total do item no carrinho com base no valor do produto
        self.preco_total = self.produto.valor * self.quantidade
        super(ItemDoCarrinho, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"

class Carrinho(models.Model):

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        # Calcula o preço total do item no carrinho com base no valor do produto
        self.preco_total = self.produto.valor * self.quantidade
        super(Carrinho, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"


class Venda(models.Model):
    numero_venda = models.IntegerField()  # Número da venda por empresa
    data_venda = models.DateField(default=date.today)  # Data da venda

    def __str__(self):
        return f"Venda #{self.numero_venda} - {self.data_venda}"

class VendaDoProduto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens', blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd = models.IntegerField(blank=True, null=True)
    data_venda = models.DateField()  # Remova auto_now_add=True
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Venda {self.venda} - Produto {self.produto.nome} - {self.qtd} unidades - Total: R${self.total} - Data {self.data_venda}"




# Função que será chamada antes de salvar uma instância de VendaDoProduto
@receiver(pre_save, sender=VendaDoProduto)
def update_total(sender, instance, **kwargs):
    # Verifica se o produto e a quantidade não são nulos e calcula o total
    if instance.produto.valor and instance.qtd:
        instance.total = instance.produto.valor * instance.qtd
    else:
        instance.total = 0  # Define total como 0 se valor ou qtd forem nulos
):
    produto = get_object_or_404(Produto, pk=produto_id)
    item, created = ItemDoCarrinho.objects.get_or_create(produto=produto)
    if item.quantidade > 1:
        item.quantidade -= 1
        item.preco_total = item.quantidade * produto.valor
        item.save()
        return redirect('index')
    else:
        item.delete()
    return redirect('index')

# View para remover todos item do carrinho
def remover_todos_do_carrinho(request, item_id):
    item = get_object_or_404(ItemDoCarrinho, pk=item_id)
    if item.quantidade >0:
        item.delete()
    return redirect('index')

