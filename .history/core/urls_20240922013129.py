from django.urls import path
from .views import * 
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('adicionar/<int:produto_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),

]
