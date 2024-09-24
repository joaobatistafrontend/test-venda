from django.db import models

class Produto(models.Model):
    produto = models.CharField(max_length=255)