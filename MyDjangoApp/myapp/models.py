from django.db import models
from django.urls import reverse

# # Create your models here.
# class Project(models.Model):
#     title=models.CharField(max_length=100)
#     description=models.TextField()
#     technology=models.CharField(max_length=20)

# # Create your models here.
class Phone(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    technology=models.CharField(max_length=20)

class Stock(models.Model):
    name=models.CharField(max_length=30)
    value=models.FloatField(null=True)
    qty=models.FloatField(null=True)
    sum=models.FloatField(null=True)
    note=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    
    # The absolute path to get the url then reverse into 'student_edit' with keyword arguments (kwargs) primary key
    def get_absolute_url(self):
        return reverse('stock_edit', kwargs={'pk': self.pk})
    
class Debt(models.Model):
    name=models.CharField(max_length=30)
    value=models.FloatField(null=True)
    qty=models.FloatField(null=True)
    sum=models.FloatField(null=True)
    note=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    
    # The absolute path to get the url then reverse into 'student_edit' with keyword arguments (kwargs) primary key
    def get_absolute_url(self):
        return reverse('debt_edit', kwargs={'pk': self.pk})    
    
class Saving(models.Model):
    name=models.CharField(max_length=30)
    value=models.FloatField(null=True)
    qty=models.FloatField(null=True)
    sum=models.FloatField(null=True)
    note=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    
    # The absolute path to get the url then reverse into 'student_edit' with keyword arguments (kwargs) primary key
    def get_absolute_url(self):
        return reverse('saving_edit', kwargs={'pk': self.pk})

class Income(models.Model):
    name=models.CharField(max_length=30)
    value=models.FloatField(null=True)
    qty=models.FloatField(null=True)
    sum=models.FloatField(null=True)
    note=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    
    # The absolute path to get the url then reverse into 'student_edit' with keyword arguments (kwargs) primary key
    def get_absolute_url(self):
        return reverse('income_edit', kwargs={'pk': self.pk})    

class Expense(models.Model):
    name=models.CharField(max_length=30)
    value=models.FloatField(null=True)
    qty=models.FloatField(null=True)
    sum=models.FloatField(null=True)
    note=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
    
    # The absolute path to get the url then reverse into 'student_edit' with keyword arguments (kwargs) primary key
    def get_absolute_url(self):
        return reverse('expense_edit', kwargs={'pk': self.pk})        
    
class StockMarket(models.Model):
    name=models.CharField(max_length=30)
    value=models.FloatField()

    def __str__(self):
        return self.name
    
class Choice(models.Model):
    name1=models.CharField(max_length=50,null=True)

