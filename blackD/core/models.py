from django.db import models


# Create your models here.


class Product(models.Model):
    nome = models.CharField(max_length=100, blank=False, )
    categoria = models.CharField(max_length=100, blank=False)
    preco_custo = models.CharField(max_length=100)
    preco_venda = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'


class Sale(models.Model):
    data = models.CharField(max_length=100, blank=False, )
    cliente = models.CharField(max_length=100, blank=False)
    total = models.CharField(max_length=100)

    def __str__(self):
        return self.cliente

    class Meta:
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'

