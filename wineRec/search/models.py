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


class UserStats(models.Model): # Saves the user and the wine list of the user
	rating = models.IntegerField(max_length=1)
	wine_id = models.IntegerField(max_length=100)
	user_id = models.CharField(max_length=100,default='shreyashshrivastava') # Superuser -> shreyashshrivastava

class Classify(models.Model): # Saves the classified categories of wines
	wine_id = models.IntegerField(max_length=100)
	class_id = models.IntegerField(max_length=100)

class knum(models.Model): # Saves the number of clusters
	num = models.IntegerField(max_length=10)

class Clusters(models.Model): # Saves the generated clusters 
	cluster_name_generated = models.TextField()

class Recommend(models.Model): # Saves the recommened wines
	rec_wine_nums = models.IntegerField(max_length=10)

class KmeansCentersUser(models.Model): # Saves the cluster centers for User generared wine clusters
	center_model_number = models.IntegerField(default=0)
	centers_user = models.FloatField()

class KmeansCentersWines(models.Model): # Saces the cluster centers for the wine categories
	centers_wines = models.FloatField()

class DistanceMetric(models.Model): # To save the clusternumber the user wants the distance metrics for
	distance_metric = models.IntegerField(default=0)

# To declare a class as an abstract class; the base class for other classes. Write the meta method.  
# # class Meta:
# 	abstract = True 