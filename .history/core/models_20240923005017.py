from django.db import models
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



Para criar uma venda no seu sistema com vários produtos, você precisará seguir alguns passos principais. Isso inclui a criação de uma instância de Venda, adição dos produtos (usando VendaDoProduto), e salvar tudo corretamente no banco de dados. Vou guiar você por esse processo, utilizando as classes que você já definiu.

Passos para criar uma venda com múltiplos produtos
Criar uma nova instância de Venda. Cada venda deve ter um número único e a data em que foi realizada.

Adicionar produtos à venda. Para cada produto que faz parte da venda, você precisa criar uma instância de VendaDoProduto, associando o produto à venda e definindo a quantidade.

Calcular o total de cada item automaticamente. A função de pre_save que você configurou já cuida disso.

Salvar tudo no banco de dados. Após adicionar todos os produtos à venda, você salva a venda e os produtos associados.

Exemplo de como implementar isso
Aqui está um exemplo de como você pode fazer isso em uma view ou dentro de um método que controla o processo de criação da venda com múltiplos produtos.

Exemplo de uma view para criar uma venda com múltiplos produtos:
python
Copiar código
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, ItemDoCarrinho, Venda, VendaDoProduto
from django.utils import timezone

def criar_venda(request):
    if request.method == 'POST':
        # Criar uma nova instância de Venda
        nova_venda = Venda.objects.create(numero_venda=get_proximo_numero_venda(), data_venda=timezone.now())

        # Buscar os itens no carrinho do usuário (simulando o processo)
        itens_do_carrinho = ItemDoCarrinho.objects.all()

        # Adicionar cada item do carrinho à venda
        for item in itens_do_carrinho:
            VendaDoProduto.objects.create(
                venda=nova_venda,
                produto=item.produto,
                qtd=item.quantidade,
                data_venda=timezone.now(),
                total=item.preco_total
            )

        # Limpar o carrinho após a venda ser finalizada
        itens_do_carrinho.delete()

        return redirect('venda_sucesso')

    return render(request, 'carrinho.html')

# Função auxiliar para gerar o próximo número de venda (pode ser específica para cada empresa se necessário)
def get_proximo_numero_venda():
    ultima_venda = Venda.objects.aggregate(Max('numero_venda'))
    proximo_numero = (ultima_venda['numero_venda__max'] or 0) + 1
    return proximo_numero
Explicação do código:
criar_venda(request): Essa função simula a criação de uma venda. No POST, ela cria uma nova instância de Venda, busca os itens no carrinho (ItemDoCarrinho), e cria uma instância de VendaDoProduto para cada item do carrinho.

get_proximo_numero_venda(): Esta função gera o próximo número de venda automaticamente, incrementando o último número de venda registrado.

Limpeza do carrinho: Após a venda ser realizada, o carrinho é esvaziado.

Atualizando o models.py se necessário
Você já possui os modelos adequados, mas pode ser interessante adicionar um método na classe Venda para calcular o total da venda somando os totais de todos os produtos. Aqui está um exemplo:

python
Copiar código
class Venda(models.Model):
    numero_venda = models.IntegerField()
    data_venda = models.DateField(default=date.today)

    def __str__(self):
        return f"Venda #{self.numero_venda} - {self.data_venda}"

    @property
    def total_venda(self):
        # Calcula o total da venda somando o total de todos os itens
        return sum(item.total for item in self.itens.all())

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
