from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
#from .models import Phone
from myapp.models import Saving,Debt,Income,Expense
#from .models import Saving as Stock 
import myapp.stockMarket
import myapp.choices as choices
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import connection
from django.views.generic import TemplateView
from django.forms import modelform_factory
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from myapp.forms import LoginForm
from django.db.models import Sum
# Create your views here.
#kullanici mehim,mert1907

@login_required
def get_charts(request):
    values=get_net_values()
    labelsSaving = []
    dataSaving = []

    labelsDebt = []
    dataDebt = []

    labelsIncome = []
    dataIncome = []

    labelsExpense = []
    dataExpense = []
    username=request.user.username
    queryset1 = Saving.objects.all()
    for saving in queryset1:
        labelsSaving.append(saving.name)
        dataSaving.append(saving.sum)

    queryset2 = Debt.objects.all()
    for debt in queryset2:
        labelsDebt.append(debt.name)
        dataDebt.append(debt.sum)

    queryset3 = Income.objects.all()
    for income in queryset3:
        labelsIncome.append(income.name)
        dataIncome.append(income.sum)

    queryset4 = Expense.objects.all()
    for expense in queryset4:
        labelsExpense.append(expense.name)
        dataExpense.append(expense.sum)        

    return render(request, 'chart.html', {
        'labelsSaving': labelsSaving,
        'dataSaving': dataSaving,
        'labelsDebt': labelsDebt,
        'dataDebt': dataDebt,
        'labelsIncome': labelsIncome,
        'dataIncome': dataIncome,
        'labelsExpense': labelsExpense,
        'dataExpense': dataExpense,
        'username':username,
        'totalSaving':values['totalSaving'],
        'totalDebt':values['totalDebt'],
        'netSaving':values['netSaving'],
        'totalIncome':values['totalIncome'],
        'totalExpense':values['totalExpense'],
        'netIncome':values['netIncome']
    })

def get_net_values():
    values=dict()
    totalSaving=Saving.objects.aggregate(Sum('sum'))
    totalDebt=Debt.objects.aggregate(Sum('sum'))
    values['totalSaving']=totalSaving['sum__sum']
    values['totalDebt']=totalDebt['sum__sum']
    values['netSaving']=totalSaving['sum__sum']-totalDebt['sum__sum']

    totalIncome=Income.objects.aggregate(Sum('sum'))
    totalExpense=Expense.objects.aggregate(Sum('sum'))
    values['totalIncome']=totalIncome['sum__sum']
    values['totalExpense']=totalExpense['sum__sum']
    values['netIncome']=totalIncome['sum__sum']-totalExpense['sum__sum']

    return(values)