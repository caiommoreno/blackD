# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blackD.core.forms import ProductForm, SaleForm
from blackD.core.models import Product, Sale
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime


@login_required
def home(request):
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
    yYear=[]
    xYear=[]
    yMonth=[]
    xMonth=[1,2,3,4,5,6,7,8,9,10,11,12]   
    yDay=[]
    xDay=[]

    try:  
        for sale in sales:            
            y = sale.year             
            xYear.append(y)          
            
    except:
        sale = Sale.objects.filter(user=usr)
        y = sale.year
        xYear.append(y)

    
    mxyear = max(xYear)
    years = [mxyear]
    y = mxyear
    for x in range(11):        
        y = y - 1
        years.append(y)
    for year in years:
        year = int(year)   
        
        if Sale.objects.filter(user=usr, year=year).count()>0:
            sale = Sale.objects.filter(user=usr, year=year)
            if sale.count()>1:
                t = 0 
                for s in sale:
                    r = s.total
                    t= t+r
                yYear.append(t)
            else:
                sale = Sale.objects.get(user=usr, year=year)    
                t = sale.total
                yYear.append(t)
        else:
            t = 0
            yYear.append(t)
        
    
    
    for m in xMonth:
        if Sale.objects.filter(user=usr, year=mxyear, month=m):
            zs = Sale.objects.filter(user=usr, year=mxyear, month=m)
            t=0
            for z in zs:
                t = t + z.total
        else:
            t=0
        yMonth.append(t) 
    

    try:
        mxmonth = max(months)
       
    except:
        sale = Sale.objects.filter(user=usr)
        mxmonth= sale.month
    daily = Sale.objects.filter(user=usr, year=mxyear, month=mxmonth)
    try:    
        for sale in daily:
            d = sale.day
            t = sale.total
            xDay.append(d)
            yDay.append(t)
    except:
        sale = Sale.objects.filter(user=usr)
        d = sale.day          
        t = sale.total            
        xDay.append(d)
        yDay.append(t)



    xYear = years
    
    xDay=[
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '20',
    '21',
    '22',
    '23',
    '24',
    '25',
    '26',
    '27',
    '28',
    '29',
    '30',
  ]

    context = {
        'sales': sales,
        'saleTot':saleTot,
        'saleAvg':saleAvg,
        'yYear':yYear,
        'xYear':xYear,
        'yMonth':yMonth,
        'xMonth':xMonth,
        'yDay':yDay,
        'xDay':xDay,           
    }

    return render(request, 'index.html', context)

@login_required
def home1(request):
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
                try:
                    x = Sale.objects.filter(user=usr, year=y)
                    for i in x:
                        dt = dict(year= i.year, total=i.total)
                        yData.append(dt)
                except:
                    pass
        
        ms = Sale.objects.filter(user=usr, year=mxyear)
        months=[]
        Months = []
        mData = []
        for m in ms:
            try:
                if m.month == 1:
                    month = "JAN"
                elif m.month == 2:
                    month = "FEB"
                elif m.month == 3:
                    month = "MAR"
                elif m.month == 4:
                    month = "APR"
                elif m.month == 5:
                    month = "MAY"
                elif m.month == 6:
                    month = "JUN"
                elif m.month == 7:
                    month = "JUL"
                elif m.month == 8:
                    month = "AUG"
                elif m.month == 9:
                    month = "SEP"
                elif m.month == 10:
                    month = "OCT"
                elif m.month == 11:
                    month = "NOV"
                elif m.month == 12:
                    month = "DEC"
                sr = month
                months.append(month)
                Months.append(m.month)           
                x = Sale.objects.filter(user=usr, month=m.month)
                mTotal = 0
                for i in x:
                    dr = dict(month=sr, total=i.total)
                    mData.append(dr)
            except:
                pass
        mxmonth = max(Months)
        days =[]
        dData = []
        ds = Sale.objects.filter(user=usr, year=mxyear, month=mxmonth)
        for d in ds:
            try:
                day = d.day
                days.append(day)
                dTotal =0
                x = Sale.objects.filter(user=usr, day=d.day)
                dTotal = 0
                for i in x:
                    dl = dict(day= i.day, total=i.total)
                    dData.append(dl)
            except:
                pass
    else:
        messages.warning(request, f"You didn't add any sales yet, please add sales to access the dashboard")
        return redirect('display_sales')
        

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