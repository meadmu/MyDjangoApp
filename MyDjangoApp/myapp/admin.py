from django.contrib import admin
from .models import Phone
from .models import Stock
from .models import StockMarket
# Register your models here.

admin.site.register(Phone)
admin.site.register(Stock)
admin.site.register(StockMarket)