from django.db import models

class Produto(models.Model):
    produto = models.CharField(max_length=255)
    valor = models.CharField(max_length=255)
    q