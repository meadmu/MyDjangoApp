from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
#from .models import Phone
from myapp.models import Saving,StockMarket,Debt
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
def SavingHomePageView(request):
    username=request.user.username
    return render(request, 'saving/savings.html', {'username':username})

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

class SavingForm(forms.ModelForm):
    note = forms.CharField(required=False)
    sum = forms.FloatField(disabled=True,required=False)
    value=forms.FloatField(disabled=True,required=False)
    qty=forms.FloatField()
    name= forms.CharField(widget=forms.Select(choices=choices.SAVING_CHOICES))
    class Meta:
        model = Saving
        fields = ('name', 'value' , 'qty','sum','note') 

@login_required
def get_saving_list(request):
    context = {}
    foo=myapp.stockMarket
    foo.WebRequest.getRequest(insert=1,clean=0,update=1)
    totalSaving=0
    savings=Saving.objects.all()
    for saving in savings:
        marketvalue = StockMarket.objects.filter(name=saving.name).values_list('value', flat = True)
        if marketvalue.exists() and saving.value is not None and saving.qty is not None:
            sum=saving.qty*marketvalue[0]
            saving.sum=sum
            totalSaving+=sum
            saving.value=marketvalue[0]
            saving.save()
    context['savings'] = savings
    context['totalval']=get_saving_sum()
    return render(request, 'saving/saving_list.html', context)

def add_saving(request):
    context = {'form': SavingForm()}
    return render(request, 'saving/add_saving.html', context)

def check_saving_value(name):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if marketvalue.exists():
        return marketvalue[0]
    return 0

def check_saving_sum(name,qty,value):
    marketvalue = StockMarket.objects.filter(name=name).values_list('value', flat = True)
    if  qty is not None:
        return marketvalue*qty
    return 0 

def add_saving_submit(request):
    context = {}
    form = SavingForm(request.POST, request.FILES)
    context['form'] = form
    if form.is_valid():
        form_=form.instance
        form_.value=check_saving_value(form_.name)
        form_.sum=form_.qty*form_.value
        context['saving'] = form.save()
        context['totalval']=get_saving_sum()
    else:
        return render(request, 'saving/add_saving.html', context)
    return render(request, 'saving/saving_row.html', context)


def add_saving_cancel(request):
    return HttpResponse()

def delete_saving(request, saving_pk):
    context={}
    saving = Saving.objects.get(pk=saving_pk)
    saving.delete()
    context['totalval']=get_saving_sum()
    return render(request, 'saving/delete_saving.html', context)

def edit_saving(request, saving_pk):
    saving = Saving.objects.get(pk=saving_pk)
    context = {}
    context['saving'] = saving
    context['form'] = SavingForm(initial={
        'name':saving.name,
        'value': saving.value,
        'qty': saving.qty,
        'sum': saving.sum,
        'note': saving.note,
    })
    return render(request, 'saving/edit_saving.html', context)

def edit_saving_submit(request, saving_pk):
    context = {}
    saving = Saving.objects.get(pk=saving_pk)
    context['saving'] = saving
    if request.method == 'POST':
        form = SavingForm(request.POST, instance=saving)
        if form.is_valid():
            new_form=form.instance
            new_form.value=check_saving_value(new_form.name)
            new_form.sum=new_form.qty*new_form.value
            new_form.save()
            context['saving'] = form.save()
            context['totalval']=get_saving_sum()
        else:
            return render(request, 'saving/edit_saving.html', context)
    return render(request, 'saving/saving_row.html', context)

def get_saving_sum():
    totalVal=Saving.objects.aggregate(Sum('sum'))
    return(totalVal['sum__sum'])

@login_required
def get_charts(request):
    labelsSaving = []
    dataSaving = []

    labelsDebt = []
    dataDebt = []
    username=request.user.username
    queryset1 = Saving.objects.all()
    for saving in queryset1:
        labelsSaving.append(saving.name)
        dataSaving.append(saving.sum)

    queryset2 = Debt.objects.all()
    for debt in queryset2:
        labelsDebt.append(debt.name)
        dataDebt.append(debt.sum)

    return render(request, 'chart.html', {
        'labelsSaving': labelsSaving,
        'dataSaving': dataSaving,
        'labelsDebt': labelsDebt,
        'dataDebt': dataDebt,
        'username':username
    })