from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('get_stocks/',views.get_stocks,name = 'Ticker'),
        path('news_with_ticker/',views.news_with_ticker,name = 'Ticker'),
        path('webscraping/',views.webscraping,name = 'Ticker'),
        path('predict/',views.predict,name = 'Ticker'),

]