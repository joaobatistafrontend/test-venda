from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto, ItemDoCarrinho, Venda, VendaDoProduto
from django.utils import timezone
from django.db.models import Max

class VendaView(TemplateView):
    template_name = 'venda.html'

    def get(self, request):
        produtos = Produto.objects.all()
        carrinho = ItemDoCarrinho.objects.all()  # Pega os itens do carrinho

        total = sum(item.produto.valor * item.quantidade for item in carrinho)
        vendas = VendaDoProduto.objects.all()


        item = ItemDoCarrinho.objects.all()

        total = sum(item.produto.valor * item.quantidade for item in carrinho)

        return render(request, self.template_name, {'produtos': produtos, 'carrinho': carrinho, 'item' : item, 'vendas' : vendas, 'total' : total,})

        

    def post(self, request):
        # Quando o botão "Adicionar ao Carrinho" for pressionado
        produto_id = request.POST.get('produto_id')
        produto = Produto.objects.get(id=produto_id)
        
        # Verifica se o item já existe no carrinho
        carrinho_item, created = ItemDoCarrinho.objects.get_or_create(produto=produto)
        
        if created:
            # Se for a primeira vez que o produto está sendo adicionado, define quantidade como 1
            carrinho_item.quantidade = 1
        else:
            # Se o item já existir no carrinho, incrementa a quantidade
            carrinho_item.quantidade += 1
        
        carrinho_item.save()  # Salva o item no carrinho com a quantidade correta
        
        # Redireciona para a mesma página após adicionar o produto
        return redirect('venda')

# Função para finalizar a venda e criar a instância de Venda e VendaDoProduto
def finalizar_venda(request):
    itens_do_carrinho = ItemDoCarrinho.objects.all()
    
    if itens_do_carrinho.exists():
        # Criar uma nova venda
        nova_venda = Venda.objects.create(numero_venda=get_proximo_numero_venda(), data_venda=timezone.now())

        # Para cada item no carrinho, cria um VendaDoProduto
        for item in itens_do_carrinho:
            VendaDoProduto.objects.create(
                venda=nova_venda,
                produto=item.produto,
                qtd=item.quantidade,
                data_venda=timezone.now(),
                total=item.produto.valor * item.quantidade
            )

        # Limpa o carrinho após a venda
        itens_do_carrinho.delete()

    return redirect('venda')  # Redireciona para a página de vendas

def get_proximo_numero_venda():
    ultima_venda = Venda.objects.aggregate(Max('numero_venda'))
    proximo_numero = (ultima_venda['numero_venda__max'] or 0) + 1
    return proximo_numero
def remover_da_venda(request, produto_id):
    empresa = Empresa.objects.filter(dono=request.user).first()
    produto = get_object_or_404(Produto, pk=produto_id, empresa=empresa)
    item = Carrinho.objects.get(produto=produto, empresa=empresa)
    
    if item.quantidade > 1:
        item.quantidade -= 1
        item.save()
    else:
        item.delete()
    
    return redirect('vendasProdutos')
