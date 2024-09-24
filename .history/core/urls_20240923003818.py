from django.urls import path
from .views import * 
from .venda import * 

urlpatterns = [
    path('', Inde.as_view(), name='venda'),




    path('adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('add_prod_carrinho/<int:produto_id>/', adicionar_no_carrinho, name='adicionar_no_carrinho'),
    path('remover_prod_carrinho/<int:produto_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('remover_todos_do_carrinho/<int:produto_id>/', remover_todos_do_carrinho, name='remover_todos_do_carrinho'),

]
