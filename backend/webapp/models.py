from django.db import models

# Create your models here.

class Stocks(models.Model):
	name = models.CharField(max_length = 30)
	price = models.FloatField()
	change = models.FloatField()
	percent_change = models.FloatField()
	volume = models.FloatField()
	avg_volume =  models.FloatField()
	market_cap = models.FloatField()
	pe_ratio = models.FloatField()

	def __str__(self):
		return "{} {} {} {} {} {} {} {}".format(self.name,self.price,self.change,self.percent_change,
													   self.volume,self.avg_volume,self.market_cap,self.pe_ratio)
