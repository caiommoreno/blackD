# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from blackD.core.Calendar import Calendar

from django.http import HttpResponse
from django.views.generic.list import ListView
from django.utils.safestring import mark_safe
from blackD.core.forms import ProductForm, SaleForm
from blackD.core.models import Product, Sale, Event
from django.contrib.auth.models import User
from django.contrib import messages
import datetime



@login_required
def empty(request):
    return redirect('home')

@login_required()
def perfil(request):
    return render(request, 'page-user.html')

@login_required
def home(request):    
    usr = request.user
    if usr.profile.is_blocked:
        messages.warning(request, f"You must pay to keep using this app")
        return redirect("PAYMENT PAGE")

    else:
        sales = Sale.objects.filter(user=usr)



        if sales.count()>0:
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
            xDay=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

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
                
            months = []
            monthly =Sale.objects.filter(user=usr, year=mxyear)
            for sale in monthly:
                month = sale.month
                months.append(month)

            
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
                sale = Sale.objects.get(user=usr)
                mxmonth= sale.month



            for d in xDay:
                if Sale.objects.filter(user=usr, year=mxyear, month=mxmonth, day=d):
                    zs = Sale.objects.filter(user=usr, year=mxyear, month=mxmonth, day=d)
                    t=0
                    for z in zs:
                        t = t + z.total
                else:
                    t=0
                yDay.append(t) 
            
            xYear = years

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
        else:
            # messages.warning(request, f"Desculpe, você precisa adicionar items na aba de 'Vendas' para usar o gráfico.")
            # return redirect('display_sales')
            year = datetime.datetime.now()
            year = year.year
            xYear = [year,]
            y = year
            for x in range(11):        
                y = y - 1
                xYear.append(y)


            xMonth=[1,2,3,4,5,6,7,8,9,10,11,12]   
            xDay=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
            saleTot=0
            saleAvg=0
            yYear=[0,0,0,0,0,0,0,0,0,0,0,0]
            yMonth=[0,0,0,0,0,0,0,0,0,0,0,0]
            yDay= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
def display_products(request):
    usr = request.user
    if usr.profile.is_blocked:
        messages.warning(request, f"You must pay to keep using this app")
        return redirect("PAYMENT PAGE")

    else:
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
    if usr.profile.is_blocked:
        messages.warning(request, f"You must pay to keep using this app")
        return redirect("PAYMENT PAGE")

    else:
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
        user = request.user

        data = request.POST.get('data')
        data = datetime.datetime.strptime(data, "%Y-%m-%d").date()
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
            user = request.user
            data = request.POST.get('data')
            data = datetime.strptime(data, "%Y-%m-%d").date()
            year = data.year
            month = data.month
            day = data.day
            cliente = request.POST.get('cliente')
            total = request.POST.get('total')

            form = Sale(pk=pk, user=user, data=data, cliente=cliente, total=total, year=year, month=month, day=day)
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



@login_required
def under_construct(request):
    return render(request, 'constructing.html')



class CalendarView(ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context



def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()