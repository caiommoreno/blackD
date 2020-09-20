from django.contrib import admin

# Register your models here.
from blackD.core.models import Product


@admin.register(Product)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_custo', 'preco_venda')
