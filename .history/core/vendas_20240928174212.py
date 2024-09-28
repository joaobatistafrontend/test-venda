from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Produto, ItemDoCarrinho, Venda, VendaDoProduto
from django.utils import timezone
from django.db.models import Max
from django.shortcuts import render, get_object_or_404


class EditarVendaProdutoView(LoginRequiredMixin, View):
    template_name = 'registration/vendas/editarVendaProduto.html'

    def get(self, request, pk):
        empresa = Empresa.objects.filter(dono=self.request.user).first()
        venda_item = get_object_or_404(VendaDoProduto, pk=pk, empresa=empresa)
        todosProdutos = Produto.objects.filter(empresa=empresa)
        carrinho = Carrinho.objects.filter(empresa=empresa)
        venda = venda_item.venda
        itens = venda.itens.all()
        total = itens.aggregate(total_venda=Sum('total'))['total_venda'] or 0

        # Verifica permissão de edição
        if venda.empresa.dono != request.user:
            return HttpResponseForbidden("Você não tem permissão para editar esta venda.")

        return render(request, self.template_name, {
            'venda': venda,
            'itens': itens,
            'venda_total': total,
            'venda_item': venda_item,
            'todosProdutos': todosProdutos,
            'carrinho': carrinho,
        })

    def post(self, request, pk):
        empresa = Empresa.objects.filter(dono=request.user).first()
        venda = get_object_or_404(VendaDoProduto, pk=pk, empresa=empresa).venda

        # Verifica permissão de edição
        if venda.empresa.dono != request.user:
            return HttpResponseForbidden("Você não tem permissão para editar esta venda.")

        produto_id = request.POST.get('produto_id')
        quantidade = 1  # Incrementa por 1 a cada clique

        # Garantir que produto_id seja válido
        if not produto_id:
            return HttpResponseBadRequest("Produto não especificado.")
    
        produto = get_object_or_404(Produto, pk=produto_id, empresa=empresa)

        # Se for edição de um item existente
        if 'editar' in request.POST:
            # Verifica se o item existe na venda
            venda_item = venda.itens.filter(produto=produto).first()
            if venda_item:
                valor_produto = venda_item.produto.valor if isinstance(venda_item.produto.valor, Decimal) else Decimal(venda_item.produto.valor)
                venda_item.qtd = quantidade
                venda_item.total = valor_produto * quantidade
                venda_item.save()
            else:
                return HttpResponseBadRequest("Item de venda não encontrado para edição.")

        # Se for adição de um novo produto
        elif 'adicionar_produto' in request.POST:
            item_existente = venda.itens.filter(produto=produto).first()
            valor_produto = produto.valor if isinstance(produto.valor, Decimal) else Decimal(produto.valor)

            if item_existente:
                item_existente.qtd += quantidade
                item_existente.total += valor_produto * quantidade
                item_existente.save()
            else:
                novo_item = VendaDoProduto(
                    venda=venda,
                    produto=produto,
                    qtd=quantidade,
                    total=valor_produto * quantidade,
                    empresa=empresa
                )
                novo_item.save()

        # Remover produto da venda
        elif 'remover_da_venda_editada' in request.POST:
            item_existente = venda.itens.filter(produto=produto).first()
            if item_existente:
                valor_produto = produto.valor if isinstance(produto.valor, Decimal) else Decimal(produto.valor)
                item_existente.qtd -= quantidade
                item_existente.total -= valor_produto * quantidade

                # Se não houver mais itens na venda, deletar a venda também
                if not venda.itens.exists():
                    venda.delete()
                    return redirect('vendas')
                if item_existente.qtd > 0:
                    item_existente.save()
                else:
                    item_existente.delete()


            else:
                return HttpResponseBadRequest("Item de venda não encontrado para remoção.")

        elif 'deleteVendaProdutos' in request.POST:
            # Obtém o item da venda que corresponde ao produto selecionado
            item_existente = venda.itens.filter(produto=produto).first()

            # Se o item existe
            if item_existente:
                item_existente.delete()
                if not venda.itens.exists():
                    venda.delete()
                    return redirect('vendas')
            if not venda.itens.exists():
                venda.delete()
                return redirect('vendas')
                # Se não há mais itens na venda, a venda pode ser deletada
            else:
                return HttpResponseBadRequest("Item de venda não encontrado para remoção.")

        return redirect('editarVendaProduto', pk=pk)
        