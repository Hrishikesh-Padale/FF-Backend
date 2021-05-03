from django.urls import path
from . import views

urlpatterns = [
        path('',views.index,name='index'),
        path('get_stocks/<str:Ticker>/',views.get_stocks,name = 'Ticker'),
]