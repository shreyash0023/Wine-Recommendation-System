from django.db import models
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
# Create your models here.

class Wine(models.Model):

	country = models.CharField(max_length =100, blank=False)
	description = models.TextField()
	designation = models.CharField(max_length =100)
	points = models.IntegerField(default=10)
	price = models.IntegerField(default=10)
	province = models.CharField(max_length =100)
	region_1 = models.CharField(max_length =100)
	region_2 = models.CharField(max_length =100)
	taster_name = models.CharField(max_length =100)
	taster_twitter_handel = models.CharField(max_length =100) 
	title = models.CharField(max_length =100, blank=False)
	variety = models.CharField(max_length =100)
	winery = models.CharField(max_length =100)


	def __str__(self): 
		return ('Name : {0} Price :{1} Points:{2}'.format(self.title,self.price,self.points))

# The rest of the models are not available. Please go to the blog to understand the implementation.





# To declare a class as an abstract class; the base class for other classes. Write the meta method.  
# # class Meta:
# 	abstract = True 