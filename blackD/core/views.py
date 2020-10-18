# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blackD.core.forms import ProductForm, SaleForm
from blackD.core.models import Product, Sale
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime


@login_required
def home1(request):
    usr = request.user
    sales = Sale.objects.filter(user=usr)
    # counting total sales
    saleTot = 0
    try:
        for sale in sales:
            saleTot = saleTot + sale.total 
    except:
        pass
    # counting sales avg
    saleAvg = 0
    try:    
        saleAvg = saleTot/sales.count()
    except:
        pass

    # create year labels list
    # create Data Matrix
    years=[]
    data=[]
    try:  
        for sale in sales:            
            y = sale.year
            m = sale.month
            d = sale.day
            t = sale.total
            dt=dict(year=y,month=m,day=d,total=t)
            years.append(y)
            data.append(dt)
    except:
        pass

    data =dict(data)
    try:
        mxyear = max(Years)
        years = [mxyear]
        y = mxyear
        for x in range(11):        
            y = y - 1
            years.append(y)
    except:
        mxyear=Years[0]

    context = {
        'sales': sales,
        'saleTot':saleTot,
        'saleAvg':saleAvg,
        'years': years,
        'data': data,
    }

    return render(request, 'index.html', context)

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

    saleAvg = 0
    try:    
        saleAvg = saleTot/sales.count()
    except:
        pass

    Years = []
    

    try:
        for sale in sales:
            year = sale.year           
            Years.append(year)
    except:
        pass
    
    if sales.count() > 0:
        mxyear = max(Years)
        years = [mxyear]
        y = mxyear
        for x in range(11):        
            y = y - 1
            years.append(y)
        yData = []        
        for y in years:
                x = Sale.objects.filter(user=usr, year=y)
                dt = dict('year': i.year, 'total':i.total)
                yData.append(dt)
        if sales.count() > 1:
            ms = Sale.objects.filter(user=usr, year=mxyear)
            months=[]
            mData = []
            for m in ms:
                month = m.month
                months.append(month)            
                x = Sale.objects.filter(user=usr, month=m)
                mTotal = 0
                for i in x:
                    dt = dict('month': i.month, 'total':i.total)
                    mData.append(dt)                    
            mxmonth = max(months)
            days =[]
            dData = []
            ds = Sale.objects.filter(user=usr, year=mxyear, month=mxmonth)
            for d in ds:
                day = d.day
                days.append(day)
                dTotal =0
                x = Sale.objects.filter(user=usr, day=d)
                dTotal = 0
                for i in x:
                    dt = dict('day': i.day, 'total':i.total)
                    dData.append(dt)                    
        else:
            ms = Sale.objects.get(user=usr)
            ms = ms.month
            months=[ms]
            ds = Sale.objects.get(user=usr)
            ds = ds.day
            days=[ds]  
            yData = [{'year': ms.year, 'total':ms.total}]
            mData = [{'month': ms.month, 'total':ms.total}]
            dData = [{'day': ms.day, 'total':ms.total}]                 
    else:
        years = 0
        months = 0
        days= 0
        yData = 0
        mData = 0
        dData = 0
        

    context = {
        'sales':sales,
        'products':products,
        'saleTot':saleTot,
        'saleAvg': saleAvg,
        'years':years,
        'months':months,
        'days':days,
        'yData': yData,
        'mData': mData,
        'dData': dData,
         
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
        data = datetime.strptime(data, "%Y-%m-%d").date()
        year = data.year
        month = data.month
        day = data.day
        cliente = request.POST.get('cliente')
        total = request.POST.get('total')

        form = Sale(user=user, data=data, cliente=cliente, total=total, year=year, month=month, day=day)
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