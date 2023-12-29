from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
#from .models import Phone
from myapp.models import Income,StockMarket,Debt
#from .models import Income as Stock 
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

username=''
def IncomeHomePageView(request):
    username=request.user.username
    return render(request, 'income/incomes.html', {'username':username})

# login page
def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, 'login.html',context={'form':AuthenticationForm()})

def user_logout(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')  

class IncomeForm(forms.ModelForm):
    note = forms.CharField(required=False)
    sum = forms.FloatField(disabled=True,required=False)
    value=forms.FloatField(disabled=True,required=False)
    qty=forms.FloatField()
    name= forms.CharField(widget=forms.Select(choices=choices.SAVING_CHOICES))
    class Meta:
        model = Income
        fields = ('name', 'value' , 'qty','sum','note') 

@login_required
def get_income_list(request):
    context = {}
    foo=myapp.stockMarket
    foo.WebRequest.getRequest(insert=0,clean=0,update=1)
    totalIncome=0
    incomes=Income.objects.all()
    for income in incomes:
        marketvalue = StockMarket.objects.filter(name=income.name).values_list('value', flat = True)
        if marketvalue.exists() and income.value is not None and income.qty is not None:
            sum=income.qty*marketvalue[0]
            income.sum=sum
            totalIncome+=sum
            income.value=marketvalue[0]
            income.save()
    context['incomes'] = incomes
    context['totalval']=get_income_sum()
    return render(request, 'income/income_list.html', context)

def add_income(request):
    context = {'form': IncomeForm()}
    return render(request, 'income/add_income.html', context)

def check_income_value(name):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if marketvalue.exists():
        return marketvalue[0]
    return 0

def check_income_sum(name,qty,value):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if  qty is not None:
        return marketvalue*qty
    return 0 

def add_income_submit(request):
    context = {}
    form = IncomeForm(request.POST, request.FILES)
    context['form'] = form
    if form.is_valid():
        form_=form.instance
        form_.value=check_income_value(form_.name)
        form_.sum=form_.qty*form_.value
        context['income'] = form.save()
        context['totalval']=get_income_sum()
    else:
        return render(request, 'income/add_income.html', context)
    return render(request, 'income/income_row.html', context)


def add_income_cancel(request):
    return HttpResponse()

def delete_income(request, income_pk):
    context={}
    income = Income.objects.get(pk=income_pk)
    income.delete()
    context['totalval']=get_income_sum()
    return render(request, 'income/delete_income.html', context)

def edit_income(request, income_pk):
    income = Income.objects.get(pk=income_pk)
    context = {}
    context['income'] = income
    context['form'] = IncomeForm(initial={
        'name':income.name,
        'value': income.value,
        'qty': income.qty,
        'sum': income.sum,
        'note': income.note,
    })
    return render(request, 'income/edit_income.html', context)

def edit_income_submit(request, income_pk):
    context = {}
    income = Income.objects.get(pk=income_pk)
    context['income'] = income
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_income_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            new_form.save()
            context['income'] = form.save()
            context['totalval']=get_income_sum()
        else:
            return render(request, 'income/edit_income.html', context)
    return render(request, 'income/income_row.html', context)

def edit_income_cancel(request,income_pk):
    context = {}
    income = Income.objects.get(pk=income_pk)
    context['income'] = income
    context['totalval']=get_income_sum()
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_income_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            new_form.save()
            context['income'] = form.save()
        else:
            return render(request, 'income/edit_income.html', context)
    return render(request, 'income/income_row.html', context)

def get_income_sum():
    totalVal=Income.objects.aggregate(Sum('sum'))
    return(totalVal['sum__sum'])

@login_required
def get_charts(request):
    labelsIncome = []
    dataIncome = []

    labelsDebt = []
    dataDebt = []
    username=request.user.username
    queryset1 = Income.objects.all()
    for income in queryset1:
        labelsIncome.append(income.name)
        dataIncome.append(income.sum)

    queryset2 = Debt.objects.all()
    for debt in queryset2:
        labelsDebt.append(debt.name)
        dataDebt.append(debt.sum)

    return render(request, 'chart.html', {
        'labelsIncome': labelsIncome,
        'dataIncome': dataIncome,
        'labelsDebt': labelsDebt,
        'dataDebt': dataDebt,
        'username':username
    })