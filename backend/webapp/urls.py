from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('get_stocks/<str:Ticker>/',views.get_stocks,name = 'Ticker'),
        path('news_with_ticker/<str:Ticker>/',views.news_with_ticker,name = 'Ticker'),
]