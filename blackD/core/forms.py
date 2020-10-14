from django import forms
from django.contrib.auth.models import User
from blackD.core.models import Product, Sale
from blackD.core.validator import validate_preco
from django.conf import settings
from datetime import datetime
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
                          input_formats=settings.DATE_INPUT_FORMATS,
                          widget=forms.DateInput(format = '%d/%m/%Y', attrs={"placeholder": "Digite aqui",
                                                                            "class": "form-control",
                                                                            'type':'date'}),
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
    def save(self, commit=True):
        date = self.data
        self.year = date.year
        self.month = date.month
        self.day = date.day

        return(year, month, day)