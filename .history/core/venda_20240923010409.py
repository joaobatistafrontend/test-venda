from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto, Carrinho, ItemDoCarrinho, Venda, VendaDoProduto
from django.utils import timezone

class VendaView(TemplateView):
    template_name = 'venda.html'

    def get(self, request):
        produtos = Produto.objects.all()
        carrinho = Carrinho.objects.all()  # Pega os itens do carrinho
        item = ItemDoCarrinho.objects.all()

        total = sum(item.preco_total for item in carrinho)

        # Criar uma venda ou pegar uma venda existente (substitua pela lógica necessária)
        venda_atual = Venda.objects.first()  # Exemplo de pegar a primeira venda. Isso dependerá da sua lógica de fluxo.

        # Pegar todos os produtos associados a essa venda
        itens_venda = VendaDoProduto.objects.filter(venda=venda_atual)

        # Calcular o total da venda somando os totais de cada item da venda
        total_venda = sum(item.total for item in itens_venda)



        return render(request, self.template_name, {
            'produtos': produtos,
            'carrinho': carrinho,
            'total_venda': total_venda,
            'venda': venda_atual,
            'itens_venda': itens_venda,
        })
    def post(self, request):
        # Quando o botão "Adicionar ao Carrinho" for pressionado
        produto_id = request.POST.get('produto_id')
        produto = Produto.objects.get(id=produto_id)
        
        # Adiciona ou atualiza o produto no carrinho
        carrinho_item, created = ItemDoCarrinho.objects.get_or_create(produto=produto)
        if not created:
            carrinho_item.quantidade += 1  # Incrementa a quantidade se o item já estiver no carrinho
        carrinho_item.save()
        
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
                total=item.preco_total
            )

        # Limpa o carrinho após a venda
        itens_do_carrinho.delete()

    return redirect('venda_sucesso')  # Redireciona para uma página de sucesso

def get_proximo_numero_venda():
    ultima_venda = Venda.objects.aggregate(Max('numero_venda'))
    proximo_numero = (ultima_venda['numero_venda__max'] or 0) + 1
    return proximo_numero
