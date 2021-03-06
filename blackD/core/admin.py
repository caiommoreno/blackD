from django.contrib import admin

# Register your models here.
from blackD.core.models import Product, Sale, Event


@admin.register(Product)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_custo', 'preco_venda')

@admin.register(Sale)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('data', 'cliente', 'total')

@admin.register(Event)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_time', 'end_time')