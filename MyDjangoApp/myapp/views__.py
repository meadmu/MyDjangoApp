from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
#from .models import Phone
from .models import Stock,StockMarket
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
from .forms import LoginForm
# Create your views here.
#kullanici mehim,mert1907


# class HomePageView(TemplateView):
#     template_name = 'home.html'

def HomePageView(request):
    username=request.user.username
    return render(request, 'home.html', {'username':username})

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

class StockForm(forms.ModelForm):
    note = forms.CharField(required=False)
    sum = forms.FloatField(disabled=True,required=False)
    value=forms.FloatField(disabled=True,required=False)
    qty=forms.FloatField()
    name= forms.CharField(widget=forms.Select(choices=choices.SAVING_CHOICES))
    class Meta:
        model = Stock
        fields = ('name', 'value' , 'qty','sum','note') 

@login_required
def get_stock_list(request):
    context = {}
    #context['stocks'] = Stock.objects.all()
    #test=Stock.objects.all().values_list()
    #test=Stock.objects.filter(name='Altın/TL').update(value=9999)
    foo=myapp.stockMarket
    foo.WebRequest.getRequest(insert=0,clean=0,update=1)
    test=Stock.objects.all()
    for item in test:
        marketvalue = StockMarket.objects.filter(name=item.name).values_list('value', flat = True)
        if marketvalue.exists() and item.value is not None and item.qty is not None:
            print('--------'+item.name+'--------'+str(marketvalue[0])+'--------')
            item.sum=item.qty*marketvalue[0]
            item.value=marketvalue[0]

    context['stocks'] = test
    return render(request, 'partial/stock/stock_list.html', context)

def add_stock(request):
    context = {'form': StockForm()}
    return render(request, 'partial/stock/add_stock.html', context)

""" def add_stock_submit(request):
    context = {}
    form = StockForm(request.POST, request.FILES)
    context['form'] = form
    if form.is_valid():
        context['stock'] = form.save()
    else:
        return render(request, 'partial/stock/add_stock.html', context)
    return render(request, 'partial/stock/stock_row.html', context) """
def check_stock_value(name):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if marketvalue.exists():
        return marketvalue[0]
    return 0

def check_stock_sum(name,qty,value):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if  qty is not None:
        return marketvalue*qty
    return 0 
""" def add_stock_submit(request):
    context = {}
    form = StockForm(request.POST, request.FILES)
    
    if form.is_valid():
        new_form=form.save(commit=False)
        new_form.value=check_stock_value(new_form.name)
        new_form.sum=new_form.qty*new_form.value
        context['form'] = new_form
        context['stock'] = new_form.save()
    else:
        return render(request, 'partial/stock/add_stock.html', context)
    return render(request, 'partial/stock/stock_row.html', context) """

def add_stock_submit(request):
    context = {}
    form = StockForm(request.POST, request.FILES)
    context['form'] = form
    if form.is_valid():
        new_form=form.instance
        new_form.value=check_stock_value(new_form.name)
        new_form.sum=new_form.qty*new_form.value
        context['stock'] = form.save()
    else:
        return render(request, 'partial/stock/add_stock.html', context)
    return render(request, 'partial/stock/stock_row.html', context)


def add_stock_cancel(request):
    return HttpResponse()

def delete_stock(request, stock_pk):
    stock = Stock.objects.get(pk=stock_pk)
    stock.delete()
    return HttpResponse()

def edit_stock(request, stock_pk):
    stock = Stock.objects.get(pk=stock_pk)
    context = {}
    context['stock'] = stock
    context['form'] = StockForm(initial={
        'name':stock.name,
        'value': stock.value,
        'qty': stock.qty,
        'sum': stock.sum,
        'note': stock.note,
    })
    return render(request, 'partial/stock/edit_stock.html', context)

def edit_stock_submit(request, stock_pk):
    context = {}
    stock = Stock.objects.get(pk=stock_pk)
    context['stock'] = stock
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_stock_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            context['stock'] = form.save()
            #form.save()
        else:
            return render(request, 'partial/stock/edit_stock.html', context)
    return render(request, 'partial/stock/stock_row.html', context)