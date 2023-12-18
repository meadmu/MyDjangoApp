from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
#from .models import Phone
from myapp.models import Debt,StockMarket
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
# Create your views here.
#kullanici mehim,mert1907


# class HomePageView(TemplateView):
#     template_name = 'home.html'

def DebtHomePageView(request):
    username=request.user.username
    return render(request, 'debt/debts.html', {'username':username})

# login page
""" def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form}) """

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
    name= forms.CharField(widget=forms.Select(choices=choices.STOCK_CHOICES))
    class Meta:
        model = Debt
        fields = ('name', 'value' , 'qty','sum','note') 

@login_required
def get_debt_list(request):
    context = {}
    #context['stocks'] = Stock.objects.all()
    #test=Stock.objects.all().values_list()
    #test=Stock.objects.filter(name='Altın/TL').update(value=9999)
    foo=myapp.stockMarket
    foo.WebRequest.getRequest(insert=0,clean=0,update=1)
    totalDebt=0
    test=Debt.objects.all()
    for item in test:
        marketvalue = StockMarket.objects.filter(name=item.name).values_list('value', flat = True)
        if marketvalue.exists() and item.value is not None and item.qty is not None:
            sum=item.qty*marketvalue[0]
            item.sum=sum
            totalDebt+=sum
            item.value=marketvalue[0]

    context['debts'] = test
    request.session['totalDebt'] = totalDebt
    response=render(request, 'debt/debt_list.html', context)
    response['HX-Trigger']='getTotalValue'
    return response

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
        new_form=form.instance
        new_form.value=check_debt_value(new_form.name)
        new_form.sum=new_form.qty*new_form.value
        context['debt'] = form.save()
    else:
        return render(request, 'debt/add_debt.html', context)
    return render(request, 'debt/debt_row.html', context)


def add_debt_cancel(request):
    return HttpResponse()

def delete_debt(request, debt_pk):
    debt = Debt.objects.get(pk=debt_pk)
    debt.delete()
    return HttpResponse()

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
            context['debt'] = form.save()
            #form.save()
        else:
            return render(request, 'debt/edit_debt.html', context)
    return render(request, 'debt/debt_row.html', context)

def get_debt_total(request):
    totalVal=""
    if 'totalDebt' in request.session:
        totalVal = str(request.session['totalDebt'])

    return render(request, 'totalValue.html', {'totalVal':totalVal})