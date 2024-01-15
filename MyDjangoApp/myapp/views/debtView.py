from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
#from .models import Phone
from myapp.models import Debt,StockMarket,Debt,Choice
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

username=''
def DebtHomePageView(request):
    username=request.user.username
    return render(request, 'debt/debts.html', {'username':username})

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

class DebtForm(forms.ModelForm):
    note = forms.CharField(required=False)
    sum = forms.FloatField(disabled=True,required=False)
    value=forms.FloatField(disabled=True,required=False)
    qty=forms.FloatField()
    name= forms.ModelChoiceField(queryset=Choice.objects.values_list('name1', flat = True),to_field_name="name1")
    class Meta:
        model = Debt
        fields = ('name', 'value' , 'qty','sum','note') 

@login_required
def get_debt_list(request):
    context = {}
    foo=myapp.stockMarket
    foo.WebRequest.getRequest(insert=0,clean=0,update=1)
    totalDebt=0
    debts=Debt.objects.all()
    for debt in debts:
        marketvalue = StockMarket.objects.filter(name=debt.name).values_list('value', flat = True)
        if marketvalue.exists() and debt.value is not None and debt.qty is not None:
            sum=debt.qty*marketvalue[0]
            debt.sum=sum
            totalDebt+=sum
            debt.value=marketvalue[0]
            debt.save()
    context['debts'] = debts
    context['totalval']=get_debt_sum()
    return render(request, 'debt/debt_list.html', context)

def add_debt(request):
    context = {'form': DebtForm()}
    return render(request, 'debt/add_debt.html', context)

def check_debt_value(name):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if marketvalue.exists():
        return marketvalue[0]
    return 0

def check_debt_sum(name,qty,value):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if  qty is not None:
        return marketvalue*qty
    return 0 

def add_debt_submit(request):
    context = {}
    form = DebtForm(request.POST, request.FILES)
    context['form'] = form
    if form.is_valid():
        form_=form.instance
        form_.value=check_debt_value(form_.name)
        form_.sum=form_.qty*form_.value
        context['debt'] = form.save()
        context['totalval']=get_debt_sum()
    else:
        return render(request, 'debt/add_debt.html', context)
    return render(request, 'debt/debt_row.html', context)


def add_debt_cancel(request):
    return HttpResponse()

def delete_debt(request, debt_pk):
    context={}
    debt = Debt.objects.get(pk=debt_pk)
    debt.delete()
    context['totalval']=get_debt_sum()
    return render(request, 'debt/delete_debt.html', context)

def edit_debt(request, debt_pk):
    debt = Debt.objects.get(pk=debt_pk)
    context = {}
    context['debt'] = debt
    context['form'] = DebtForm(initial={
        'name':debt.name,
        'value': debt.value,
        'qty': debt.qty,
        'sum': debt.sum,
        'note': debt.note,
    })
    return render(request, 'debt/edit_debt.html', context)

def edit_debt_submit(request, debt_pk):
    context = {}
    debt = Debt.objects.get(pk=debt_pk)
    context['debt'] = debt
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_debt_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            new_form.save()
            context['debt'] = form.save()
            context['totalval']=get_debt_sum()
        else:
            return render(request, 'debt/edit_debt.html', context)
    return render(request, 'debt/debt_row.html', context)

def edit_debt_cancel(request,debt_pk):
    context = {}
    debt = Debt.objects.get(pk=debt_pk)
    context['debt'] = debt
    context['totalval']=get_debt_sum()
    if request.method == 'POST':
        form = DebtForm(request.POST, instance=debt)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_debt_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            new_form.save()
            context['debt'] = form.save()
        else:
            return render(request, 'debt/edit_debt.html', context)
    return render(request, 'debt/debt_row.html', context)

def get_debt_sum():
    totalVal=Debt.objects.aggregate(Sum('sum'))
    return(totalVal['sum__sum'])

@login_required
def get_charts(request):
    labelsDebt = []
    dataDebt = []

    labelsDebt = []
    dataDebt = []
    username=request.user.username
    queryset1 = Debt.objects.all()
    for debt in queryset1:
        labelsDebt.append(debt.name)
        dataDebt.append(debt.sum)

    queryset2 = Debt.objects.all()
    for debt in queryset2:
        labelsDebt.append(debt.name)
        dataDebt.append(debt.sum)

    return render(request, 'chart.html', {
        'labelsDebt': labelsDebt,
        'dataDebt': dataDebt,
        'labelsDebt': labelsDebt,
        'dataDebt': dataDebt,
        'username':username
    })