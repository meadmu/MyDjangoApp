from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
#from .models import Phone
from myapp.models import Expense,StockMarket,Debt
#from .models import Expense as Stock 
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
def ExpenseHomePageView(request):
    username=request.user.username
    return render(request, 'expense/expenses.html', {'username':username})

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

class ExpenseForm(forms.ModelForm):
    note = forms.CharField(required=False)
    sum = forms.FloatField(disabled=True,required=False)
    value=forms.FloatField(disabled=True,required=False)
    qty=forms.FloatField()
    name= forms.CharField(widget=forms.Select(choices=choices.SAVING_CHOICES))
    class Meta:
        model = Expense
        fields = ('name', 'value' , 'qty','sum','note') 

@login_required
def get_expense_list(request):
    context = {}
    foo=myapp.stockMarket
    foo.WebRequest.getRequest(insert=0,clean=0,update=1)
    totalExpense=0
    expenses=Expense.objects.all()
    for expense in expenses:
        marketvalue = StockMarket.objects.filter(name=expense.name).values_list('value', flat = True)
        if marketvalue.exists() and expense.value is not None and expense.qty is not None:
            sum=expense.qty*marketvalue[0]
            expense.sum=sum
            totalExpense+=sum
            expense.value=marketvalue[0]
            expense.save()
    context['expenses'] = expenses
    context['totalval']=get_expense_sum()
    return render(request, 'expense/expense_list.html', context)

def add_expense(request):
    context = {'form': ExpenseForm()}
    return render(request, 'expense/add_expense.html', context)

def check_expense_value(name):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if marketvalue.exists():
        return marketvalue[0]
    return 0

def check_expense_sum(name,qty,value):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if  qty is not None:
        return marketvalue*qty
    return 0 

def add_expense_submit(request):
    context = {}
    form = ExpenseForm(request.POST, request.FILES)
    context['form'] = form
    if form.is_valid():
        form_=form.instance
        form_.value=check_expense_value(form_.name)
        form_.sum=form_.qty*form_.value
        context['expense'] = form.save()
        context['totalval']=get_expense_sum()
    else:
        return render(request, 'expense/add_expense.html', context)
    return render(request, 'expense/expense_row.html', context)


def add_expense_cancel(request):
    return HttpResponse()

def delete_expense(request, expense_pk):
    context={}
    expense = Expense.objects.get(pk=expense_pk)
    expense.delete()
    context['totalval']=get_expense_sum()
    return render(request, 'expense/delete_expense.html', context)

def edit_expense(request, expense_pk):
    expense = Expense.objects.get(pk=expense_pk)
    context = {}
    context['expense'] = expense
    context['form'] = ExpenseForm(initial={
        'name':expense.name,
        'value': expense.value,
        'qty': expense.qty,
        'sum': expense.sum,
        'note': expense.note,
    })
    return render(request, 'expense/edit_expense.html', context)

def edit_expense_submit(request, expense_pk):
    context = {}
    expense = Expense.objects.get(pk=expense_pk)
    context['expense'] = expense
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_expense_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            new_form.save()
            context['expense'] = form.save()
            context['totalval']=get_expense_sum()
        else:
            return render(request, 'expense/edit_expense.html', context)
    return render(request, 'expense/expense_row.html', context)

def edit_expense_cancel(request,expense_pk):
    context = {}
    expense = Expense.objects.get(pk=expense_pk)
    context['expense'] = expense
    context['totalval']=get_expense_sum()
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_expense_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            new_form.save()
            context['expense'] = form.save()
        else:
            return render(request, 'expense/edit_expense.html', context)
    return render(request, 'expense/expense_row.html', context)

def get_expense_sum():
    totalVal=Expense.objects.aggregate(Sum('sum'))
    return(totalVal['sum__sum'])

@login_required
def get_charts(request):
    labelsExpense = []
    dataExpense = []

    labelsDebt = []
    dataDebt = []
    username=request.user.username
    queryset1 = Expense.objects.all()
    for expense in queryset1:
        labelsExpense.append(expense.name)
        dataExpense.append(expense.sum)

    queryset2 = Debt.objects.all()
    for debt in queryset2:
        labelsDebt.append(debt.name)
        dataDebt.append(debt.sum)

    return render(request, 'chart.html', {
        'labelsExpense': labelsExpense,
        'dataExpense': dataExpense,
        'labelsDebt': labelsDebt,
        'dataDebt': dataDebt,
        'username':username
    })