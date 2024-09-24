from django.db import models

class NovaCategoria(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.nome}'


class Produto(models.Model):
    
    produto = models.CharField(max_length=100, blank=True, null=True)
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
        return f"{self.quantidade} x {self.produto}"

class Carrinho(models.Model):

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        # Calcula o preço total do item no carrinho com base no valor do produto
        self.preco_total = self.produto.valor * self.quantidade
        super(Carrinho, self).save(*args, **kwargs)

    def __str__(self):
        return f"empresa: {self.empresa} - {self.quantidade} x {self.produto.nome_produto}"
    