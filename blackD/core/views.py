# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blackD.core.forms import ProductForm, SaleForm
from blackD.core.models import Product, Sale
from django.contrib.auth.models import User
from django.contrib import messages


@login_required
def home(request):
    usr = request.user
    sales = Sale.objects.filter(user=usr)
    products = Product.objects.filter(user=usr)
    saleTot = 0
    try:
        for sale in sales:
            saleTot = saleTot + sale.total 
    except:
        pass

    saleAvg = saleTot/sales.count()

    years = []
    try:
        for sale in sales:
            date = sale.data
            year=date.split('/')[2]
            years.append(year)
    except:
        pass

    context = {
        'sales':sales,
        'products':products,
        'saleTot':saleTot,
        'saleAvg': saleAvg,
        'years':years,
        
    }

    return render(request, 'index.html', context)


@login_required
def display_products(request):
    usr = request.user
    items = Product.objects.filter(user=usr)
    if request.method == 'POST':
        if request.POST.get('delete') == '':
            pk = request.POST.get('pk')
            prod = Product.objects.filter(id=pk)
            prodUser = request.POST.get('prodUser')
            if usr.username == prodUser:
                Product.objects.filter(id=pk).delete()
            else:
                messages.warning(request, f"You are not autharized to delete this item")

    context = {
        'items': items,
    }
    return render(request, 'products.html', context)

@login_required
def display_sales(request):
    usr = request.user
    items = Sale.objects.filter(user=usr)
    if request.method == 'POST':
        if request.POST.get('delete') == '':
            pk = request.POST.get('pk')
            sl = Sale.objects.filter(id=pk)
            slUser = request.POST.get('slUser')
            if usr.username == slUser:
                Sale.objects.filter(id=pk).delete()
            else:
                messages.warning(request, f"You are not autharized to delete this item")
    context = {
        'items': items,
    }
    return render(request, 'sales.html', context)


@login_required
def add_product(request):
    if request.method == 'POST':
        # form = ProductForm(request.POST)
        user = request.user

        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        preco_custo = request.POST.get('preco_custo')
        preco_venda = request.POST.get('preco_venda')

        form = Product(user=user, nome=nome, categoria=categoria, preco_custo=preco_custo, preco_venda=preco_venda)
        form.save()
        return redirect('display_products')

    else:
        form = ProductForm()
        return render(request, 'add_item.html', {'form': form, 'header': 'Adicionar Produtos'})


@login_required
def add_sales(request):
    if request.method == 'POST':
        # form = ProductForm(request.POST)
        user = request.user

        data = request.POST.get('data')
        cliente = request.POST.get('cliente')
        total = request.POST.get('total')

        form = Sale(user=user, data=data, cliente=cliente, total=total)
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
            form = ProductForm(request.POST, instance=item)
            if form.is_valid():
                try:
                    form.save()
                    return redirect('display_products')
                except:
                    pass
            else:
                return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Produtos'})
        else:
            form = ProductForm(instance=item)
            return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Produtos'})
    else:
        messages.warning(request, f"You are not autharized to edit this item")        

        form = ProductForm(instance=item)
        return render(request, 'add_item.html', {'form': form, 'header': 'Editando Produtos'})


@login_required
def edit_sales(request, pk):
    item = get_object_or_404(Sale, pk=pk)
    usr = request.user
    if item.user == usr:
        if request.method == 'POST':
            form = SaleForm(request.POST, instance=item)
            if form.is_valid():

                try:
                    form.save()
                    return redirect('display_sales')
                except:
                    messages.warning(request, f"something is wrong")
            else:
                return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Vendas'})

                form.save()
                return redirect('display_sales')

        else:
            form = SaleForm(instance=item)
            return render(request, 'edit_item.html', {'form': form, 'header': 'Editando Vendas'})

    else:
        messages.warning(request, f"You are not autharized to edit this item")
        form = SaleForm(instance=item)
        return render(request, 'add_item.html', {'form': form, 'header': 'Editando Vendas'})




@login_required
def delete_sales(request, pk):
    usr = request.user
    sl = Sale.objects.filter(id=pk)
    if usr == sl.user:
        Sale.objects.filter(id=pk).delete()
    else:
        messages.warning(request, f"You are not autharized to delete this item")

    items = Sale.objects.all()

    context = {
        'items': items
    }
    return render(request, 'sales.html', context)

@login_required
def delete_product(request, pk):
    usr = request.user
    sl = Product.objects.filter(id=pk)
    if usr == sl.user:
        Product.objects.filter(id=pk).delete()
    else:
        messages.warning(request, f"You are not autharized to delete this item")

    items = Sale.objects.all()

    context = {
        'items': items
    }
    return render(request, 'sales.html', context)