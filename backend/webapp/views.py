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
	#add_stock()	#add stock instances
	objects = Stocks.objects.all()
	serializer = StocksSerializer(objects,many=True) #serialize 
	#print(serializer.data[:10])
	return Response(serializer.data) #render the json 

@api_view(['GET'])
def parameter(request,parameter):
	#print(parameter,parameter[13:])
	if "company_name" in parameter:
		cname = parameter[13:]
		objects = Stocks.objects.filter(name__contains=cname)
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "price>" in parameter:
		p = parameter[6:]
		objects = Stocks.objects.filter(price__gt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "price<" in parameter:
		p = parameter[6:]
		objects = Stocks.objects.filter(price__lt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "price=" in parameter:
		p = parameter[6:]
		objects = Stocks.objects.filter(price=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "change>" in parameter:
		p = parameter[7:]
		objects = Stocks.objects.filter(change__gt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "change<" in parameter:
		p = parameter[7:]
		objects = Stocks.objects.filter(change__lt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "change=" in parameter:
		p = parameter[7:]
		objects = Stocks.objects.filter(change=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "percent_chg>" in parameter:
		p = parameter[12:]
		objects = Stocks.objects.filter(percent_change__gt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "percent_chg<" in parameter:
		p = parameter[12:]
		objects = Stocks.objects.filter(percent_change__lt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "percent_chg=" in parameter:
		p = parameter[12:]
		objects = Stocks.objects.filter(percent_change=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "volume>" in parameter:
		p = parameter[7:]
		objects = Stocks.objects.filter(volume__gt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "volume<" in parameter:
		p = parameter[7:]
		objects = Stocks.objects.filter(volume__lt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "volume=" in parameter:
		p = parameter[7:]
		objects = Stocks.objects.filter(volume=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "avg_vol>" in parameter:
		p = parameter[8:]
		print("param:",parameter)
		objects = Stocks.objects.filter(avg_volume__gt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "avg_vol<" in parameter:
		p = parameter[8:]
		objects = Stocks.objects.filter(avg_volume__lt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "avg_vol=" in parameter:
		p = parameter[8:]
		objects = Stocks.objects.filter(avg_volume=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "market_cap>" in parameter:
		p = parameter[11:]
		objects = Stocks.objects.filter(market_cap__gt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "market_cap<" in parameter:
		p = parameter[11:]
		objects = Stocks.objects.filter(market_cap__lt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "market_cap=" in parameter:
		p = parameter[11:]
		objects = Stocks.objects.filter(market_cap=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "pe_ratio>" in parameter:
		p = parameter[9:]
		objects = Stocks.objects.filter(pe_ratio__gt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "pe_ratio<" in parameter:
		p = parameter[9:]
		objects = Stocks.objects.filter(pe_ratio__lt=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)

	elif "pe_ratio=" in parameter:
		p = parameter[9:]
		objects = Stocks.objects.filter(pe_ratio=float(p))
		serializer = StocksSerializer(objects,many=True)
		return Response(serializer.data)


	return HttpResponse("No parameters given")

#function to add stock instances of model Stocks
def add_stock():
	with open('C:/Users/padal/Desktop/FF-Backend/backend/webapp/data.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			name = row[0]
			price = row[1][:-1]
			change = row[2][:-1]
			percent_change = row[3][:-1]
			volume = row[4][:-1]
			avg_volume = float(row[5][:-1].replace(",","."))
			market_cap = row[6][:-1]
			if "N/A" in row[7]:
				pe_ratio = 0.0
			else:
				pe_ratio = float(row[7].replace(",",""))
			new_stock = Stocks(name=name,price=price,change=change,percent_change=percent_change,
							   volume=volume,avg_volume=avg_volume,market_cap=market_cap,pe_ratio=pe_ratio)
			new_stock.save()
	

