from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto, ItemDoCarrinho, Venda, VendaDoProduto
from django.utils import timezone
from django.db.models import Max
from django.shortcuts import render, get_object_or_404


class Vendas