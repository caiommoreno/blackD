from django import forms
from django.contrib.auth.models import User
from blackD.core.models import Product, Sale
from blackD.core.validator import validate_preco


class ProductForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label='Nome')
    categoria = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label='Categoria')
    preco_custo = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}),
                                  label='Preço Custo',)
    preco_venda = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label='Preço Venda',
                                     )

    class Meta:
        model = Product
        fields = ('user','nome', 'categoria', 'preco_custo', 'preco_venda')
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'



class SaleForm(forms.ModelForm):
    data = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label='Data')
    cliente = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}),
                                  label='Cliente',)
    total = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label='Total',
                                     )

    class Meta:
        model = Sale
        fields = ('data', 'cliente', 'total')
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'
