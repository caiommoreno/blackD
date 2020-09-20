from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect

from blackG.core.forms import ProductForm
from blackG.core.models import Product


def home(request):
    return render(request, 'index.html')


def display_products(request):
    items = Product.objects.all()
    context = {
        'items': items,
    }
    return render(request, 'products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_products')
    else:
        form = ProductForm()
        return render(request, 'add_products.html', {'form': form})


