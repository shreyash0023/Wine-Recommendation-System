
# This file has been intentionally hampered with! Please go to the blog to understand the implementation.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate 
from django.contrib.auth import get_user_model, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
import re
## https://www.julienphalip.com/blog/adding-search-to-a-django-site-in-a-snap/ ##

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
data = pd.read_csv("WineDataSet_train.csv") 
print(data)
			




def login_view(request):
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)
	if form.is_vaild():
		username = form.clean_data.get('username')
		password = form.clean_data.get('password')
		user = authenticate(username=username,password=password)
		login(request,user)
		if next:
			return redirect(next)
		else:
			return redirect('/')

	context = {
	'form':form

	}

	return render(request,'search/index.html',context)


def index(request):
	return render(request,'search/index.html')

@login_required
def display_wine(request): 
	items_list = Wine.objects.all().order_by('?')
	query = request.GET.get('q')
	type_query = request.GET.get('dropdown')


	## TF-IDF SEARCH



	# Displaying collection
	user_name = request.user.username
	user_name = (str)(user_name)
	wines_from_user = UserStats.objects.filter(user_id=user_name)

	idlist_of_selected_wines = []

	# Classify Wine (Kmeans)


	# To check if clusters are made (clusters exist in the database)
	check_cluster = 0
	if len(knum.objects.all()) != 0:
		check_cluster = 1
	else:
		check_cluster = 0




	# To invoke the classification function
	if classify_num != None and classify_num != '':
		clusters_num = (int)(classify_num)

	# Store the number of clusters entered by the user in the database
	if classify_num != None and change_cluster==1:
		if len(knum.objects.all()) != 0:
			knum.objects.all().delete()
		knum.objects.create(num=classify_num)

	cluster_names_arr = []

	model_Kmeans = 0
	
	# Invoke classify only whe the clusters are changed

	if classify_num != None and change_cluster == 1:
		knum.objects.all().delete()
		knum.objects.create(num=classify_num)

		def classify(clusters_num):

			description = data['description']
			train = description

			kmeans = KMeans(n_clusters=clusters_num)
			vectorizer = TfidfVectorizer(stop_words='english')
			X = vectorizer.fit_transform(train.values.astype('U'))
			true_k = clusters_num +1
			model = KMeans(n_clusters=true_k, init='k-means++', max_iter=5, n_init=1)
			model.fit(X)
			model_Kmeans = model

			#print("Top terms per cluster:")
			order_centroids = model.cluster_centers_.argsort()[:, ::-1]

			terms = vectorizer.get_feature_names()
			for i in range(true_k):
			    #print("Cluster %d:" % i),
			    for ind in order_centroids[i, :1]:
			        #print(' %s' % terms[ind]),
			        cluster_names_arr.append(terms[ind])
			    #print
			


			# Remove previous classification
			if len(Classify.objects.all())> 0:
				Classify.objects.all().delete()

			# Adding wine classifed categories to winedata set 

			count = 0
			for x in model.labels_[:10000]:
				Classify.objects.create(wine_id=count,class_id=x)
				count+=1


		classify(clusters_num)
		# Remive nan's
		if len(cluster_names_arr) > 0:
			for x in cluster_names_arr:
				if x == 'nan':
					cluster_names_arr.remove(x)
		# Capitalize
		if len(cluster_names_arr) >0:
			for x in range(len(cluster_names_arr)):
				cluster_names_arr[x] =  cluster_names_arr[x].capitalize()


		
		# Store the cluster names in the database 
		# Delete the previous cluster names
		Clusters.objects.all().delete()
		# Add the new clusters to the database
		for x in cluster_names_arr:
			Clusters.objects.create(cluster_name_generated=x)


	collection_display_id = 0
	for x in Clusters.objects.all():
		if x.cluster_name_generated == classify_display:
			break
		else:
			collection_display_id+=1

	cluster_collection_display_list = []
	add_to_collection = 0
	if collection_display == 1:

		for x in Classify.objects.all():
				if x.class_id == collection_display_id:
					cluster_collection_display_list.append(Wine.objects.all()[add_to_collection])
				add_to_collection+=1
		# for x in Wine.objects.all()
		# 	if Wine.id in 


		paginator = Paginator(cluster_collection_display_list,10) # Show 5 wines per page

		page = request.GET.get('page')
	  


	rec_items = []
	wine_rec_items = []
	appedd_isTrue = 0
	if len(Recommend.objects.all()) != 0:
		for x in Recommend.objects.all():
			wine_rec_items = Classify.objects.filter(class_id=x.rec_wine_nums)
 
			if len(wine_rec_items) != 0:
				wine_rec_item = wine_rec_items[0].wine_id

				try:
					rec_items.append(Wine.objects.get(id=wine_rec_item))
					appedd_isTrue =1
				except Wine.DoesNotExist:
					pass

	rec_onnn = 0

	if len(Recommend.objects.all()) >0 and len(UserStats.objects.all().filter(user_id=request.user.username)) >0:
		rec_onnn = 1
	else:
		rec_onnn = 0

	final_recommendation = []

	for x in rec_items:
		if x not in final_recommendation:
			final_recommendation.append(x)	

	

	context = {
		'items':items,
		'name':request.user.username,
		'query1': request.GET.get('dropdown'),
		'query2': type(type_query),
		'rating':UserStats.objects.all(),
		'collection': selected_wines[:maxlen],
		'wine_id': item_ids,
		'len':maxlen,
		'exists':exists,
		'cluster_names':Clusters.objects.all(),
		'check_cluster':check_cluster,
		'collection_display': collection_display,
		'cluster_collection_display_list':cluster_collection_display_list,
		'recommend_wines':final_recommendation,
		'display':display_categoty,
		'recc_on': rec_onnn
		

	}
	

	return render(request,'search/products.html',context)


def add_wine(request):
	if request.method == 'POST':
		form = WineForm(request.POST)

		if form.is_vaild():
			form.save()
			return redirect('products')
 
	else:
		form = WineForm()
		return render(request,'add_new.html',{'form':form})

def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('accounts:login')

def wineDetails_view(request,id):
	get_data = Wine.objects.get(id=id)
	des = get_data.description
	whole_data = Wine.objects.all()
	
	des_list = []

	for x in range(10):
		des_list.append(whole_data[x])
	
	last = des[-1:]
	if last != '.':
		des +='.'

	user_name = request.user.username
	user_name = (str)(user_name)
	exists = 0
	if len(UserStats.objects.filter(wine_id=id ,user_id=user_name)) != 0:
		exists = 1
	else:
		exists = 0

	if 'del' in request.POST:
		UserStats.objects.filter(wine_id__icontains=id, user_id__icontains=user_name).delete()
		


	rating = request.GET.get('dropdown')
	
	if rating != None:
		rating = str(rating)
		
		rating = (int)(rating)
		user_name = request.user.username
		user_name = (str)(user_name)
		UserStats.objects.create(rating=rating,wine_id=id,user_id=user_name)
		userss = (UserStats.objects.filter(user_id=user_name))
		for x in userss:
			print(x.wine_id,x.rating,x.user_id)


	context = {'item': get_data,
	'name':request.user.username,
	'des':des,
	'l':last,
	'll':get_data.description,
	'test':rating,
	'id':id,
	'exists':exists,
	'twitter': len(get_data.taster_twitter_handel)

	 }
	

	 # Deleting 


	return render(request,'search/details.html',context)








# Create your views here.