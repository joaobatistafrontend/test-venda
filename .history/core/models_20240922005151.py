from django.db import models

class NovaCategoria(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.nome}'


class Produto(models.Model):
    nome = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_categoria = models.ForeignKey(NovaCategoria, on_delete=models.CASCADE)
    


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

from django.db.models import Max


class Venda(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    numero_venda = models.IntegerField()  # Número da venda por empresa
    data_venda = models.DateField(default=date.today)  # Data da venda

    def __str__(self):
        return f"Venda #{self.numero_venda} - {self.data_venda}"

    def save(self, *args, **kwargs):
        if not self.numero_venda:
            ultima_venda = Venda.objects.filter(empresa=self.empresa).aggregate(Max('numero_venda'))
            ultimo_numero_venda = ultima_venda['numero_venda__max']
            self.numero_venda = (ultimo_numero_venda or 0) + 1
        super().save(*args, **kwargs)
class VendaDoProduto(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens', blank=True, null=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    qtd = models.IntegerField(blank=True, null=True)
    data_venda = models.DateField()  # Remova auto_now_add=True
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Dados adicionais da solicitação
    cliente_nome = models.CharField(max_length=255, blank=True, null=True)
    cliente_endereco = models.CharField(max_length=255, blank=True, null=True)
    cliente_ponto_referencia = models.CharField(max_length=255, blank=True, null=True)
    cliente_telefone = models.CharField(max_length=20, blank=True, null=True)
    tipo_entrega = models.CharField(max_length=50, blank=True, null=True)
    pagamento = models.CharField(max_length=50, blank=True, null=True)
    troco = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True, default='Pendente')

    def __str__(self):
        return f"{self.empresa} - Venda {self.venda} - Produto {self.produto.nome_produto} - {self.qtd} unidades - Total: R${self.total} - Cliente: {self.cliente_nome} - Data {self.data_venda}"




# Função que será chamada antes de salvar uma instância de VendaDoProduto
@receiver(pre_save, sender=VendaDoProduto)
def update_total(sender, instance, **kwargs):
    # Verifica se o produto e a quantidade não são nulos e calcula o total
    if instance.produto.valor and instance.qtd:
        instance.total = instance.produto.valor * instance.qtd
    else:
        instance.total = 0  # Define total como 0 se valor ou qtd forem nulos
