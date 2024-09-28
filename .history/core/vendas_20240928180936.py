from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Venda, Produto, VendaDoProduto
from django.shortcuts import render, redirect

class VendasView(TemplateView):
    template_name = 'vendas.html'

    def get(self, request, pk):
        venda = get_object_or_404(Venda, pk=pk)
        produtos = Produto.objects.all()

        return render(request, self.template_name, {
            'venda': venda,
            'produtos': produtos
        })

    def post(self, request, pk):
        venda = get_object_or_404(Venda, pk=pk)
        produto_id = request.POST.get('produto_id')
        acao = request.POST.get('acao')

        # Adicionar produto à venda
        if acao == 'adicionar':
            produto = get_object_or_404(Produto, id=produto_id)
            item_venda, created = VendaDoProduto.objects.get_or_create(
                venda=venda, produto=produto,
                defaults={'qtd': 1, 'total': produto.valor, 'data_venda': venda.data_venda}
            )
            if not created:
                item_venda.qtd += 1
                item_venda.total = item_venda.qtd * produto.valor
                item_venda.save()

        # Remover produto da venda
        elif acao == 'remover':
            item_venda = get_object_or_404(VendaDoProduto, venda=venda, produto__id=produto_id)
            if item_venda.qtd > 1:
                item_venda.qtd -= 1
                item_venda.total = item_venda.qtd * item_venda.produto.valor
                item_venda.save()
            else:
                item_venda.delete()

            # Verificar se a venda ainda tem itens
            if not venda.itens.exists():  # Se não houver mais itens na venda
                venda.delete()
                return redirect('venda')  # Redireciona para a lista de vendas, ou outro lugar

        return redirect('edita_venda', pk=venda.pk)
