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
from django.contrib.auth.decorators import login_required
import myapp.views as views
from myapp.views.savingView import (
    HomePageView, 
    get_stock_list,
    add_stock,
    add_stock_submit,
    add_stock_cancel,
    edit_stock,
    edit_stock_submit,
    delete_stock,
    user_login,
    user_logout,
    get_stock_total
)
from myapp.views.debtView import (
    DebtHomePageView, 
    get_debt_list,
    add_debt,
    add_debt_submit,
    add_debt_cancel,
    edit_debt,
    edit_debt_submit,
    delete_debt,
    get_debt_total
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('savings', login_required(HomePageView), name='home'),
    path('get_stock_list', get_stock_list, name='get_stock_list'),
    path('add_stock', add_stock, name='add_stock'),
    path('add_stock_submit', add_stock_submit, name='add_stock_submit'),
    path('add_stock_cancel', add_stock_cancel, name='add_stock_cancel'),
    path('<int:stock_pk>/delete_stock', delete_stock, name='delete_stock'),
    path('<int:stock_pk>/edit_stock', edit_stock, name='edit_stock'),
    path('<int:stock_pk>/edit_stock_submit', edit_stock_submit, name='edit_stock_submit'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('debts', login_required(DebtHomePageView), name='debts'),
    path('get_debt_list', get_debt_list, name='get_debt_list'),
    path('add_debt', add_debt, name='add_debt'),
    path('add_debt_submit', add_debt_submit, name='add_debt_submit'),
    path('add_debt_cancel', add_debt_cancel, name='add_debt_cancel'),
    path('<int:debt_pk>/delete_debt', delete_debt, name='delete_debt'),
    path('<int:debt_pk>/edit_debt', edit_debt, name='edit_debt'),
    path('<int:debt_pk>/edit_debt_submit', edit_debt_submit, name='edit_debt_submit'),
    path('get_debt_total', get_debt_total, name='get_debt_total'),
    path('get_stock_total', get_stock_total, name='get_stock_total'),
    path('', views.savingView.chart, name='pie-chart'),
    ]