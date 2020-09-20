from django import forms

from blackG.core.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('nome', 'categoria', 'preco_custo', 'preco_venda')
