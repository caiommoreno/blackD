"""blackD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from blackD.core.views import home, display_products, display_sales, add_product, add_sales, edit_sales, delete_sales, edit_product, delete_product, under_construct, empty, perfil, CalendarView
from blackD.pagamento.views import pagseguro_notification, create_subscription_invoice

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', empty),
    path('calendar/', CalendarView.as_view(), name ='calendar'),
    path('visaogeral', home, name='home'),
    path('perfil/', perfil, name='perfil'),
    #path('', include("blackD.authentication.urls")),
    path('produtos/', display_products, name='display_products'),
    path('add_products/', add_product, name='add_product'),
    path('edit_products/<int:pk>/', edit_product, name='edit_product'),
    path('delete_products/<int:pk>/', delete_product, name='delete_product'),
    path('vendas/', display_sales, name='display_sales'),
    path('add_sales/', add_sales, name='add_sales'),
    path('edit_sales/<int:pk>/', edit_sales, name='edit_sales'),
    path('delete_sales/<int:pk>/', delete_sales, name='delete_sales'),
    path('', include('blackD.users.urls')),
    path('constructing/', under_construct, name='constructing'),
    path('pagseguro_notification', pagseguro_notification, name='pagseguro_notification'),
    path('create_subscription_invoice', create_subscription_invoice, name='create_subscription_invoice')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

