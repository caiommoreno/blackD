# Create your views here.
from datetime import datetime
from functools import wraps

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from schedule import utils as schedule_utils
from blackD.core.services import (
    get_user_calendar, get_calendar_occurrences, create_event, update_event, cancel_occurrences as cancel_event_occurrences
)
from blackD.core.forms import ProductForm, SaleForm
from blackD.core.serializers import EventSerializer, CancelOccurrencesSerializer
from blackD.core.models import Product, Sale
from django.contrib.auth import get_user_model
from django.contrib import messages

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import SessionAuthentication

User = get_user_model()


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
            year = datetime.now()
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


class CalendarView(TemplateView):
    template_name = 'calendar.hml.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar = get_user_calendar(self.request.user)
        context["calendar"] = calendar
        context["events"] = list(calendar.events.all())
        return context


class EventPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        calendar = get_user_calendar(request.user)
        return calendar.events.filter(id=obj.id).exists()


class EventViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSerializer
    lookup_field = "id"
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, EventPermission]

    def get_queryset(self):
        calendar = get_user_calendar(self.request.user)
        return calendar.events.all()

    def create(self, request, *args, **kwargs):
        input_ser = self.get_serializer(data=request.data)
        input_ser.is_valid(raise_exception=True)

        event = create_event(
            calendar_slug=self.request.user.username,
            user=self.request.user,
            title=input_ser.validated_data["title"],
            description=input_ser.validated_data.get("description"),
            start=input_ser.to_start(),
        )
        ser = self.get_serializer(instance=event)
        return Response(data=ser.data, status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        event = self.get_object()
        serializer = self.get_serializer(event, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        event.start = serializer.to_start()
        update_event(event)

        out_ser = self.get_serializer(instance=event)
        return Response(data=out_ser.data)

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=["post"])
    def cancel_occurrences(self, request, **kwargs):
        serializer = CancelOccurrencesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = self.get_object()
        after_date = serializer.validated_data.get("after_dt")
        cancel_event_occurrences(event, after_date)
        return Response()
