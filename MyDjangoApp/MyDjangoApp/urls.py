"""
URL configuration for MyDjangoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from myapp.views import (
    HomePageView, 
    get_stock_list,
    add_stock,
    add_stock_submit,
    add_stock_cancel,
    edit_stock,
    edit_stock_submit,
    delete_stock
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('get_stock_list', get_stock_list, name='get_stock_list'),
    path('add_stock', add_stock, name='add_stock'),
    path('add_stock_submit', add_stock_submit, name='add_stock_submit'),
    path('add_stock_cancel', add_stock_cancel, name='add_stock_cancel'),
    path('<int:stock_pk>/delete_stock', delete_stock, name='delete_stock'),
    path('<int:stock_pk>/edit_stock', edit_stock, name='edit_stock'),
    path('<int:stock_pk>/edit_stock_submit', edit_stock_submit, name='edit_stock_submit')
    ]