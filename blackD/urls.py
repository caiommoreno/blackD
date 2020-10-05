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

from blackD.core.views import home, display_products, display_sales, add_product, add_sales, edit_product, edit_sales, \
    delete_product, delete_sales

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    #path('', include("blackD.authentication.urls")),
    path('products/', display_products, name='display_products'),
    path('add_products/', add_product, name='add_product'),
    path('edit_products/<int:pk>/', edit_product, name='edit_product'),
    path('delete_products/<int:pk>/', delete_product, name='delete_product'),
    path('sales/', display_sales, name='display_sales'),
    path('add_sales/', add_sales, name='add_sales'),
    path('edit_sales/<int:pk>/', edit_sales, name='edit_sales'),
    path('delete_sales/<int:pk>/', delete_sales, name='delete_sales'),
    path('user/', include('blackD.users.urls')),

]

