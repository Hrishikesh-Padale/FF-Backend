from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *

# Create your views here.

def index(request):
	return render(request,'webapp/index.html')

#function to add stock instances of model Stocks
def add_stock():
	name = "SBI"
	price = 371.10
	change = 4.15
	percent_change = 1.12
	volume = 25.339
	avg_volume = 50.82
	market_cap = 3.311
	pe_ratio = 14.28
	new_stock = Stocks(name=name,price=price,change=change,percent_change=percent_change,
					   volume=volume,avg_volume=avg_volume,market_cap=market_cap,pe_ratio=pe_ratio)

	new_stock.save()
	

