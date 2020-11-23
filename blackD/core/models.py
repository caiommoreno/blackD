from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=100, blank=False, )
    cliente = models.CharField(max_length=100, blank=False)
    total = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()

    def __str__(self):
        return self.cliente

    class Meta:
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title