from django.db import models

class NovaCategoria(models.Model):
    nome = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.nome}'


class Produto(models.Model):
    produto = models.CharField(max_length=100, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tipo_categoria = models.ForeignKey(NovaCategoria, on_delete=models.CASCADE)