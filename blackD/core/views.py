# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blackD.core.forms import ProductForm, SaleForm
from blackD.core.models import Product, Sale
from django.contrib.auth.models import User

@login_required
def home(request):
    return render(request, 'index.html')

@login_required
def display_products(request):
    usr = request.user
    items = Product.objects.filter(user=usr)
    context = {
        'items': items,
    }
    return render(request, 'products.html', context)

@login_required
def display_sales(request):
    usr = request.user
    items = Sale.objects.filter(user=usr)
    context = {
        'items': items,
    }
    return render(request, 'sales.html', context)

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form.user=request.user
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
        form.user = request.user

        if form.is_valid():
            form.save()
            return redirect('display_sales')

    else:
        form = SaleForm()
        return render(request, 'add_item.html', {'form': form, 'header': 'Adicionar Vendas'})

@login_required
def edit_product(request, pk):
    item = get_object_or_404(Product, pk=pk)
    usr = request.user
    if item.user == usr:
        if request.method == 'POST':
            form = ProductForm(request.POST, instance = item)
            if form.is_valid():
                form.save()
                return redirect('display_products')
        else:
            form = ProductForm(instance=item)
            return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Produtos'})
    else:
        message(request, f"You are not autharized to edit this item")        

@login_required
def edit_sales(request, pk):
    item = get_object_or_404(Sale, pk=pk)
    usr = request.user
    if item.user == usr:
        if request.method == 'POST':
            form = SaleForm(request.POST, instance=item)
            if form.is_valid():
                form.save()
                return redirect('display_sales')

        else:
            form = SaleForm(instance=item)
            return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Vendas'})
    else:
        message(request, f"You are not autharized to edit this item") 


@login_required
def delete_product(request, pk):
    usr = request.user
    prod = Product.objects.filter(id=pk)
    if usr == prod.user:
        Product.objects.filter(id=pk).delete()
    else:
        message(request, f"You are not autharized to delete this item")

    items = Product.objects.all()

    context = {
        'items': items
    }
    return render(request, 'products.html', context)

@login_required
def delete_sales(request, pk):
    usr = request.user
    sl = Sale.objects.filter(id=pk)
    if usr == sl.user:
        Sale.objects.filter(id=pk).delete()
    else:
        message(request, f"You are not autharized to delete this item")
    

    items = Sale.objects.all()

    context = {
        'items': items
    }
    return render(request, 'sales.html', context)