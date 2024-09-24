from django.urls import path
from .views import * 
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('<slug:empresa_slug>/add_prod_carrinho/<int:produto_id>/', adicionar_no_carrinho, name='adicionar_no_carrinho'),

]
