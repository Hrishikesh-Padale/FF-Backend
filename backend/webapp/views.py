from django.shortcuts import render,redirect
from django.http import HttpResponse
from webapp.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import json
import requests
from monkeylearn import MonkeyLearn
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from .ml_model import *
from .SAnalyser import *

# def load_sentiment_model():
# 	MODEL = load_model(f'/home/{getpass.getuser()}/Desktop/FF-Backend/backend/webapp/templates/webapp/sentiment_data/SA.h5')

SA = SAnalysis()

#Create your views here.
#API to get the stocks by Ticker -->Arguments required = Ticker , start="2017-01-01", end="2017-04-30"
@api_view(['GET'])
def get_stocks(request,Ticker):
	data = yf.download(tickers=Ticker,period='1d', interval='1m')
	asset = pd.DataFrame(data['Adj Close'])
	#plt.plot(asset, color='red', linewidth=2)
	#plt.title('BTX Performance')
	#plt.ylabel('Price ($)')
	#plt.xlabel('Date')
	#plt.show()
	json = data.to_json(orient='records')

	#response to be returned to frontend
	return Response(json)

def index(request):
	return HttpResponse("Index Page")

#API to get top headlines from a particular ticker input by scrapping function
@api_view(['GET'])
def news_with_ticker(request,Ticker):
	url='https://finance.yahoo.com/quote/{}'.format(str(Ticker))	
	r = requests.get(url)
	soup=BeautifulSoup(r.text,'html.parser')
	if(soup):
		price = soup.find('table',{'class': 'W(100%)'}).find("tbody")
		price2=price.find('tr',{'data-reactid':'40'})
		price3=price.find('tr',{'data-reactid':'45'})
		if(price2 !=None and price3!=None):
			url = ('https://newsapi.org/v2/everything?'
			       'q={}&'
			       'from=2021-05-02&'
			       'sortBy=popularity&'
			       'apiKey=e42cf979dc004ba6abfca80bb7fce05d'.format(str(Ticker))) # enter api key
			
			ml= MonkeyLearn("3fa9643fa860ec3e9376994cd1fc534b850d4c7d") # enter api key
			model_id = 'cl_pi3C7JiL' # keep model id same
			response = requests.get(url)
			json_dict=(response.json())
			sentiment=[]
			data = {}
			data['Details'] = []
			for i in range(10):
				sentiment.append(json_dict['articles'][i]['description'])
					
			for i in range(len(sentiment)):
				result = ml.classifiers.classify(model_id,[sentiment[i]])
				data['Details'].append({
			    	'Date': '2021-04-22',
			    	'Tikr': '{}'.format(str(Ticker)),
			    	'Text': str(result.body[0]['text']),
			    	'Sentiment': str(result.body[0]['classifications'][0]['tag_name']),
			    	'Previous Close':str(price2.text.replace("Previous Close","")),
			    	'Open':str(price3.text.replace("Open",""))
				})

			output = []
			j = 1
			for i in data['Details']:
				output.append({j:i['Text']})
				j += 1
			

			#response to be returned to frontend -> json format
			#returning as rest_framework response for react JS
			return Response(output)
	else:
		return HttpResponse("Not Found")



def specialcharrem(text):
	textrem5=text.replace("\\","")
	textrem4=textrem5.replace("\"","")
	textrem2=textrem4.replace("\n",'')
	textrem3=textrem2.replace("\r",'')
	textrem=textrem3.replace("<ol><li>",'');
	cleanr = re.compile(r'<[^>]+>')
	cleantext = re.sub(cleanr, '',textrem)
	string_encode = cleantext.encode("ascii", "ignore")
	string_decode = string_encode.decode()
	#print(string_decode)	
	return string_decode


@api_view(['GET'])	
def webscrapping(request,Ticker):
	url=f'https://finance.yahoo.com/quote/{Ticker}'	
	#print("Tick name" +str(list2[c]))
	r = requests.get(url)
	soup=BeautifulSoup(r.text,'html.parser')
	if(soup):
		price = soup.find('table',{'class': 'W(100%)'}).find("tbody")
		price2=price.find('tr',{'data-reactid':'40'})
		price3=price.find('tr',{'data-reactid':'45'})
		if(price2 !=None and price3!=None):
			url = ('https://newsapi.org/v2/everything?'
			       f'q={Ticker}&'
			       'from=2021-05-02&'
			       'sortBy=popularity&'
			       'apiKey=9a88c0422d2745318025da04a984d41c') # enter api key
			
			ml= MonkeyLearn("002b6c923eae7affc804cd7fdce19221871bf78d") # enter api key
			model_id = 'cl_pi3C7JiL' # keep model id same
			response = requests.get(url)
			json_dict=(response.json())
			sentiment=[]
			data = {}
			data['Details'] = []
			for i in range(10):
				sentiment.append(json_dict['articles'][i]['description'])
					
			for i in range(len(sentiment)):
				result = ml.classifiers.classify(model_id,[sentiment[i]])
				data['Details'].append({
			    	'Date': '2021-04-22',
			    	'Tikr': Ticker,
			    	'Text': specialcharrem(str(result.body[0]['text'])),
			    	'Sentiment': str(result.body[0]['classifications'][0]['tag_name']),
			    	'Previous Close':str(price2.text.replace("Previous Close","")),
			    	'Open':str(price3.text.replace("Open",""))
				})

			
			sentiment_output = []
			for sentence in data['Details']:
				sentiment_output.append(SA.SentimentAnalyzer(sentence['Text'])[0])

			zerocount = 0
			onecount = 0
			twocount = 0
			print(sentiment_output)
			for i in sentiment_output:
				if np.argmax(i) == 0:
					zerocount += 1
				elif np.argmax(i) == 1:
					onecount += 1
				elif np.argmax(i) == 2:
					twocount += 1

			percent_values = {"Negativity":(zerocount/10)*100,"Neutrality":(onecount/10)*100,"Positivity":(twocount/10)*100}
			print(percent_values)

			return Response([percent_values])




#import ML module 
@api_view(['GET'])
def predict(request,Ticker):
	obj = TechnicalPricePrediction(Ticker)
	output = obj.predict()
	output = [{"Prediction Result":output}]
	return Response(output)




'''@api_view(['GET'])
def index(request):
	if not Stocks.objects.all():
		add_stock()	#add stock instances
	objects = Stocks.objects.all()
	serializer = StocksSerializer(objects,many=True) #serialize 
	#print(serializer.data[:10])
	print(type(serializer))
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
'''

