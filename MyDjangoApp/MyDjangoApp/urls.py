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
    edit_saving_cancel,
)
from myapp.views.debtView import (
    DebtHomePageView, 
    get_debt_list,
    add_debt,
    add_debt_submit,
    add_debt_cancel,
    edit_debt,
    edit_debt_submit,
    edit_debt_cancel,
    delete_debt,
)

from myapp.views.incomeView import (
    IncomeHomePageView, 
    get_income_list,
    add_income,
    add_income_submit,
    add_income_cancel,
    edit_income,
    edit_income_submit,
    edit_income_cancel,
    delete_income,
)
from myapp.views.expenseView import (
    ExpenseHomePageView, 
    get_expense_list,
    add_expense,
    add_expense_submit,
    add_expense_cancel,
    edit_expense,
    edit_expense_submit,
    edit_expense_cancel,
    delete_expense,
)

from myapp.views.chartView import (
get_charts,
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
    path('<int:saving_pk>/edit_saving_cancel', edit_saving_cancel, name='edit_saving_cancel'),
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
    path('<int:debt_pk>/edit_debt_cancel', edit_debt_cancel, name='edit_debt_cancel'),
    path('expenses', login_required(ExpenseHomePageView), name='expenses'),
    path('get_expense_list', get_expense_list, name='get_expense_list'),
    path('add_expense', add_expense, name='add_expense'),
    path('add_expense_submit', add_expense_submit, name='add_expense_submit'),
    path('add_expense_cancel', add_expense_cancel, name='add_expense_cancel'),
    path('<int:expense_pk>/delete_expense', delete_expense, name='delete_expense'),
    path('<int:expense_pk>/edit_expense', edit_expense, name='edit_expense'),
    path('<int:expense_pk>/edit_expense_submit', edit_expense_submit, name='edit_expense_submit'),
    path('<int:expense_pk>/edit_expense_cancel', edit_expense_cancel, name='edit_expense_cancel'),
    path('incomes', login_required(IncomeHomePageView), name='incomes'),
    path('get_income_list', get_income_list, name='get_income_list'),
    path('add_income', add_income, name='add_income'),
    path('add_income_submit', add_income_submit, name='add_income_submit'),
    path('add_income_cancel', add_income_cancel, name='add_income_cancel'),
    path('<int:income_pk>/delete_income', delete_income, name='delete_income'),
    path('<int:income_pk>/edit_income', edit_income, name='edit_income'),
    path('<int:income_pk>/edit_income_submit', edit_income_submit, name='edit_income_submit'),
    path('<int:income_pk>/edit_income_cancel', edit_income_cancel, name='edit_income_cancel'),
    path('', get_charts, name='pie-chart'),
    ]