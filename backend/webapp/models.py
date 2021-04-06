from django.db import models

# Create your models here.

class Stocks(models.Model):
	name = models.CharField(max_length = 30)
	price = models.CharField(max_length = 30)
	change = models.CharField(max_length = 30)
	percent_change = models.CharField(max_length = 30)
	volume = models.CharField(max_length = 30)
	avg_volume =  models.CharField(max_length = 30)
	market_cap = models.CharField(max_length = 30)
	pe_ratio = models.CharField(max_length = 30)

	def __str__(self):
		return "{} {} {} {} {} {} {} {}".format(self.name,self.price,self.change,self.percent_change,
													   self.volume,self.avg_volume,self.market_cap,self.pe_ratio)
