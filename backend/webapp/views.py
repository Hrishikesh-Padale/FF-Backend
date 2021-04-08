from django.shortcuts import render,redirect
from django.http import HttpResponse
from webapp.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
import csv

# Create your views here.

@api_view(['GET'])
def index(request):
	add_stock()	#add stock instances
	objects = Stocks.objects.all()
	serializer = StocksSerializer(objects,many=True) #serialize 
	#print(type(serializer.data))
	return Response(serializer.data) #render the json 


#function to add stock instances of model Stocks
def add_stock():
	with open('C:/Users/padal/Desktop/FF-Backend/backend/webapp/data.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			name = row[0]
			price = row[1]
			change = row[2]
			percent_change = row[3]
			volume = row[4]
			avg_volume = row[5]
			market_cap = row[6]
			pe_ratio = row[7]
			new_stock = Stocks(name=name,price=price,change=change,percent_change=percent_change,
							   volume=volume,avg_volume=avg_volume,market_cap=market_cap,pe_ratio=pe_ratio)
			new_stock.save()
	

