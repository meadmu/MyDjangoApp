from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Phone
from .models import Stock
import myapp.stockMarket
from django.contrib.auth import get_user_model
from django.db import connection
from django.views.generic import TemplateView
# Create your views here.
#kullanici mehim,mert1907
def hello(request):

   #foo_instance =Phone.objects.create(title='TestTitle',description='TestDescription',technology='TestTechnology')
   template = loader.get_template('hello.html')
   foo=myapp.stockMarket
   foo.WebRequest.getRequest(run=1,clean=0)
   cursor = connection.cursor()
   # cursor.execute('''SELECT count(*) FROM stock''')
   # row = cursor.fetchone()
   # print (row)
   '''table = """INSERT INTO stock (
               name,
               value) VALUES (%s,%f); 
            """
   dataset = ("para",90.556)
   t1="'vmert'"
   t2=90.4656
   cursor.execute(f"INSERT INTO myapp_stock(name,value) VALUES ('{dataset[0]}',{dataset[1]});")
   print("Table is Ready")
   
   # Close the connection
   cursor.close()'''


   """ if request.method == 'POST':
        #form = Top_List_Form(request.POST)
        print(request.POST)
        return render(request, "hello.html")
   else:
      return render(request, "hello.html") """
   
   if 'unsubscribe' in request.POST:
        print(request.POST)
        return render(request, "hello.html")
   else:
      return render(request, "hello.html")


