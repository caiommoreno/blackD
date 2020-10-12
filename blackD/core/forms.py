from django import forms
from django.contrib.auth.models import User
from blackD.core.models import Product, Sale
from blackD.core.validator import validate_preco


class ProductForm(forms.ModelForm):
    nome = forms.CharField(label='Nome',
                           widget=forms.TextInput(attrs={"placeholder": "Digite aqui",
                                                         "class": "form-control"}))

    categoria = forms.CharField(label='Categoria',
                                widget=forms.TextInput(attrs={"placeholder": "Digite aqui",
                                                              "class": "form-control"}))

    preco_custo = forms.IntegerField(label='Preço de Custo',
                                     widget=forms.NumberInput(attrs={"placeholder": "Digite aqui",
                                                                     "class": "form-control"}))

    preco_venda = forms.IntegerField(label='Preço de Venda',
                                     widget=forms.NumberInput(attrs={"placeholder": "Digite aqui",
                                                                     "class": "form-control"}))

    class Meta:
        model = Product
        fields = ('nome', 'categoria', 'preco_custo', 'preco_venda')
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'


class SaleForm(forms.ModelForm):
    data = forms.DateField(label='Data',
                           widget=forms.DateInput(format='%d/%m/%Y', attrs={"placeholder": "Digite aqui ",
                                                                            "class": "form-control"}),
                           )

    cliente = forms.CharField(label='Cliente',
                              widget=forms.TextInput(attrs={"placeholder": "Digite aqui",
                                                            "class": "form-control"})
                              )

    total = forms.IntegerField(label='Total',
                               widget=forms.NumberInput(attrs={"placeholder": "Digite aqui",
                                                               "class": "form-control"})
                               )

    class Meta:
        model = Sale
        fields = ('data', 'cliente', 'total')
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'
