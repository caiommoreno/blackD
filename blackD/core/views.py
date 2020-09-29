# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from blackD.core.forms import ProductForm, SaleForm
from blackD.core.models import Product, Sale


def home(request):
    return render(request, 'index.html')


def display_products(request):
    items = Product.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'products.html', context)


def display_sales(request):
    items = Sale.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'sales.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('display_products')

    else:
        form = ProductForm()
        return render(request, 'add_item.html', {'form': form, 'header': 'Adicionar Produtos'})


def add_sales(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('display_sales')

    else:
        form = SaleForm()
        return render(request, 'add_item.html', {'form': form, 'header': 'Adicionar Vendas'})


def edit_product(request, pk):
    item = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance = item)
        if form.is_valid():
            form.save()
            return redirect('display_products')

    else:
        form = ProductForm(instance=item)
        return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Produtos'})


def edit_sales(request, pk):
    item = get_object_or_404(Sale, pk=pk)

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('display_sales')

    else:
        form = SaleForm(instance=item)
        return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Vendas'})


def delete_product(request, pk):
    Product.objects.filter(id=pk).delete()

    items = Product.objects.all()

    context = {
        'items': items
    }
    return render(request, 'products.html', context)


def delete_sales(request, pk):
    Sale.objects.filter(id=pk).delete()

    items = Sale.objects.all()

    context = {
        'items': items
    }
    return render(request, 'sales.html', context)