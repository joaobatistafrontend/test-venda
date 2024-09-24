from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'
    def get(self, request):
        produtos = Produto.objects.all()

        return render(request, self.template_name, {'produtos':produtos})
    

