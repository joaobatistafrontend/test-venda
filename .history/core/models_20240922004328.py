from django.db import models

class NovaCategoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.nome}'


class Produto(models.Model):
    produto = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    q