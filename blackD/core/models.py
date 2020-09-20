from django.db import models


# Create your models here.


class Product(models.Model):
    nome = models.CharField(max_length=100, blank=False)
    categoria = models.CharField(max_length=100, blank=False)
    preco_custo = models.IntegerField()
    preco_venda = models.IntegerField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'
