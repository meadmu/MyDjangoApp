from django.contrib import admin
from .models import (Stock,StockMarket,Debt,Choice)
from .models import Stock
from .models import StockMarket
# Register your models here.


admin.site.register(Stock)
admin.site.register(StockMarket)
admin.site.register(Debt)
admin.site.register(Choice)