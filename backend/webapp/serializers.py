from rest_framework import serializers
from webapp.models import *

class StocksSerializer(serializers.ModelSerializer):
	class Meta:
		model = Stocks
		fields = ('name','price','change','percent_change','volume','avg_volume','market_cap','pe_ratio')