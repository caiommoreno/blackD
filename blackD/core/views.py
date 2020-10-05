# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blackD.core.forms import ProductForm, SaleForm
from blackD.core.models import Product, Sale

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def display_products(request):
    
    items = Product.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'products.html', context)

@login_required
def display_sales(request):
    items = Sale.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'sales.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('display_products')

    else:
        form = ProductForm()
        return render(request, 'add_item.html', {'form': form, 'header': 'Adicionar Produtos'})

@login_required
def add_sales(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('display_sales')

    else:
        form = SaleForm()
        return render(request, 'add_item.html', {'form': form, 'header': 'Adicionar Vendas'})

@login_required
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

@login_required
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

@login_required
def delete_product(request, pk):
    Product.objects.filter(id=pk).delete()

    items = Product.objects.all()

    context = {
        'items': items
    }
    return render(request, 'products.html', context)

@login_required
def delete_sales(request, pk):
    Sale.objects.filter(id=pk).delete()

    items = Sale.objects.all()

    context = {
        'items': items
    }
    return render(request, 'sales.html', context)