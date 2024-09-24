from django.db import models

class NovaCategoria(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'empresa {self.empresa} - {self.nome}'


class Produto(models.Model):
    produto = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    q