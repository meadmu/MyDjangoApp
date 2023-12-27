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
    SavingHomePageView, 
    get_saving_list,
    add_saving,
    add_saving_submit,
    add_saving_cancel,
    edit_saving,
    edit_saving_submit,
    delete_saving,
    user_login,
    user_logout,
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
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('savings', login_required(SavingHomePageView), name='home'),
    path('get_saving_list', get_saving_list, name='get_saving_list'),
    path('add_saving', add_saving, name='add_saving'),
    path('add_saving_submit', add_saving_submit, name='add_saving_submit'),
    path('add_saving_cancel', add_saving_cancel, name='add_saving_cancel'),
    path('<int:saving_pk>/delete_saving', delete_saving, name='delete_saving'),
    path('<int:saving_pk>/edit_saving', edit_saving, name='edit_saving'),
    path('<int:saving_pk>/edit_saving_submit', edit_saving_submit, name='edit_saving_submit'),
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
    path('', views.savingView.get_charts, name='pie-chart'),
    ]