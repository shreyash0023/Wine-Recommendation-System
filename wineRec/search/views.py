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
from django.http import JsonResponse
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics import adjusted_rand_score
data = pd.read_csv("WineDataSet_train.csv") 

#print(data)

# Kmeans Cluster centers 
kmeans_cluster_centers_users = []
kmeans_cluster_centers_wines = []



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

	def normalize_query(query_string,findterms=re.compile(r'"([^"]+)"|(\S+)').findall,normspace=re.compile(r'\s{2,}').sub):
  		return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


	def get_query(query_string, search_fields):

		query = None # Query to search for every search term        
		terms = normalize_query(query_string)
		
		index = [] 
		for x in range(len(terms)):
			if terms[x] == 'wines' or terms[x] == 'Wines' or terms[x] == 'Wine' or terms[x] == 'wine':
				index.append(x)

		for x in index:
			terms.pop(x)


		for term in terms:
			or_query = None # Query to search for a given term in each field
			for field_name in search_fields:
				q = Q(**{"%s__icontains" % field_name: term})
				if or_query is None:
					or_query = q
				else:
					or_query = or_query | q
			if query is None:
				query = or_query
			else:
				query = query & or_query
		return query

	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']

		entry_query = get_query(query_string, ['description'])

		found_entries = Wine.objects.filter(entry_query).order_by('-price')

	## TF-IDF SEARCH ENDS 

	if query:
		if type_query == 'country':
			items_list = items_list.filter( 
				Q(country__icontains=query) 
				)
		elif type_query == 'title':
			items_list = items_list.filter( 
				Q(title__icontains=query) 
				)
		elif type_query == 'price_above':
			query = int(query)
			items_list = items_list.filter( 
				price__gte=query
				)
		elif type_query == 'price_below':
			query = int(query)
			items_list = items_list.filter( 
				price__lte=query
				)
		elif type_query == 'points_above':
			query = int(query)
			items_list = items_list.filter( 
				points__gte=query
				)
		elif type_query == 'points_below':
			query = int(query)
			items_list = items_list.filter( 
				points__lte=query
				)
		elif type_query == 'province':
			items_list = items_list.filter( 
				Q(province__icontains=query) 
				)
		elif type_query == 'variety':
			items_list = items_list.filter( 
				Q(variety__icontains=query) 
				)
		elif type_query == 'winery':
			items_list = items_list.filter( 
				Q(winery__icontains=query) 
				)
		elif type_query == 'exhaustive':
			items_list = found_entries
			
        	

	paginator = Paginator(items_list,5) # Show 5 wines per page

	page = request.GET.get('page')
  

	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)

	#num = len(items)


	# Displaying collection
	user_name = request.user.username
	user_name = (str)(user_name)
	wines_from_user = UserStats.objects.filter(user_id=user_name)

	idlist_of_selected_wines = []

	for x in wines_from_user:
		idlist_of_selected_wines.append(x.wine_id)

	wine_list = Wine.objects.all()

	selected_wines = []
	for x in wine_list:
		if x.id in idlist_of_selected_wines:
			selected_wines.append(x)


	item_ids = []
	for x in wine_list:
		if x.id in idlist_of_selected_wines:
			item_ids.append(x.id)

	maxlen = 0

	for x in selected_wines:
		maxlen+=1

	if maxlen > 10:
		maxlen=10

	exists = 0
	if len(UserStats.objects.filter(user_id=user_name)) != 0:
		exists = 1
	else:
		exists = 0
	#print(exists)


	# Classify Wine (Kmeans)
	def classify():
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

		#print(data['country'][:10])

		description = data['description']
		train = description

		kmeans = KMeans(n_clusters=5)
		vectorizer = TfidfVectorizer(stop_words='english')
		X = vectorizer.fit_transform(train.values.astype('U'))
		true_k = 10
		model = KMeans(n_clusters=true_k, init='k-means++', max_iter=5, n_init=1)
		model.fit(X)

		print("Top terms per cluster:")
		order_centroids = model.cluster_centers_.argsort()[:, ::-1]
		#print((model.labels_))




		terms = vectorizer.get_feature_names()
		for i in range(true_k):
		    print("Cluster %d:" % i),
		    for ind in order_centroids[i, :1]:
		        print(' %s' % terms[ind]),
		    print


	# print("\n")
	# print("Prediction")
	# print(type(data['description'][3]))
	# Y = vectorizer.transform([data['description'][3]])
	# prediction = model.predict(Y)
	# print(prediction)

	classify_num = request.GET.get('catnum',None) # gets the number of categories (int)
	classify_display = request.GET.get('cat',None) # gets the category to display (str)
	display_categoty = (str)(classify_display)
	#Check if the clusters are changed

	new_cluster_num = 0
	for x in knum.objects.all():
		new_cluster_num = (int)(x.num)

	change_cluster = 0

	
	if (classify_num) != None:
		classify_num = str(classify_num)
		if classify_num!= '':
			if new_cluster_num != (int)(classify_num):
				change_cluster = 1 
			else:
				change_cluster = 0

	# if classify_num != Null
	# classify_num = (int)(classify_num)


	# To display the clusters if invoked
	collection_display = 0
	if classify_display != None:
		collection_display = 1
	else:
		collection_display = 0


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
			model = KMeans(n_clusters=true_k, init='k-means++', max_iter=10, n_init=1)
			model.fit(X)
			model_Kmeans = model

			#kmeans_cluster_centers_wines = model.cluster_centers_
			#print(len(kmeans_cluster_centers_wines))
			#print("Top terms per cluster:")

			# Deleting previous culster centers 
			if len(KmeansCentersWines.objects.all()) != 0:
				KmeansCentersWines.objects.all().delete()

			# Adding the cluster centers (distance) to the database (After converting it to string)
			for x in range(len(model.cluster_centers_)):
				for y in (model.cluster_centers_[x]):
					KmeansCentersUser.objects.create(center_model_number=x,centers_user=y)
				


			# for x in model.cluster_centers_:
			# 	KmeansCentersWines.objects.create(centers_wines=float(x))

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


		paginator = Paginator(cluster_collection_display_list,10) # Show 10 wines per page

		page = request.GET.get('page')
	  

		try:
			cluster_collection_display_list = paginator.page(page)
		except PageNotAnInteger:
			cluster_collection_display_list = paginator.page(1)
		except EmptyPage:
			cluster_collection_display_list = paginator.page(paginator.num_pages)


	# Recommendation system 
	recomended_wines = []
	predicted_classes = []

	if 'rec' in request.POST:
		def recommend(clusters_num):

			description = data['description']
			train = description

			kmeans = KMeans(n_clusters=clusters_num)
			vectorizer = TfidfVectorizer(stop_words='english')
			X = vectorizer.fit_transform(train.values.astype('U'))
			true_k = clusters_num +1
			model = KMeans(n_clusters=true_k, init='k-means++', max_iter=5, n_init=1)
			model.fit(X)
			model_Kmeans = model
			#print(len(model.cluster_centers_))
			for x in UserStats.objects.all():
				title_to_convert = str(Wine.objects.get(id=x.wine_id).title)
				Y = vectorizer.transform([title_to_convert])
				predicted_classes.append((int)(model_Kmeans.predict(Y)))
				Recommend.objects.create(rec_wine_nums=(int)(model_Kmeans.predict(Y)))
		# if len(knum.objects.all()) != 0:
		# 	recommend((knum.objects.num))
		# print(len(UserStats.objects.all()))

		rec_num = 0
		for x in knum.objects.all():
			rec_num = x.num
		recommend(rec_num)
		


	if 'rec_del' in request.POST:
		Recommend.objects.all().delete()


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

	
	super_user = 0 

	if request.user.username == 'shreyashshrivastava':
		super_user=1
	else:
		super_user=0

	
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
		'recc_on': rec_onnn,
		'super':super_user
		

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
		# for x in userss:
		# 	print(x.wine_id,x.rating,x.user_id)


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
	


	return render(request,'search/details.html',context)


from django.urls import path
## Statistical Analysis (Wine Categories and their graphs)


from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
User = get_user_model()


class HomeView(View):
	def get(self, request, *args, **kwargs):
		
		print(request.GET.get('cat'))
		count = 0 
		cluster_arr = []
		for x in Clusters.objects.all():
			cluster_arr.append(str(x.cluster_name_generated))

		count = 0
		for x in cluster_arr:
			if str(request.GET.get('cat')) == x:
				break
			count+=1
		
		DistanceMetric.objects.create(distance_metric=count)

		return render(request,'search/charts.html', {"customers": 10,"name":request.user,'cluster_names':Clusters.objects.all()})



def get_data(request, *args, **kwargs):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response


class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		qs_count = User.objects.all().count()
	

		clusters_name = Clusters.objects.all()
		cluster_name_arr = []

		class_id = Classify.objects.all()
		for x in clusters_name:
			#print(x.cluster_name_generated)
			cluster_name_arr.append(x.cluster_name_generated)

		class_ids = []
		class_ids_count = []

		for x in class_id:
			class_ids.append(x.class_id)

		for x in range(max(class_ids)+1):
			count = 0
			for y in ((class_ids)):
				if x == y:
					count+=1
			class_ids_count.append(count)


		label_count = []
		for x in range(len(class_ids_count)):
			label_count.append([cluster_name_arr[class_ids[x]-1],class_ids_count[x]])

		final_labels = []
		final_count = []
		for x in range(len(label_count)-1):
			if label_count[x][0] != 'Wine' and  label_count[x][1] != 0:
				final_labels.append(label_count[x][0])
				final_count.append(label_count[x][1])


		labels = final_labels
		default_items = final_count

	
		data_distance = []

		
		metric = 0 

		if len(DistanceMetric.objects.all()) != 0:
			for x in DistanceMetric.objects.all():
				metric = x.distance_metric

		for x in KmeansCentersUser.objects.all().filter(center_model_number=metric):
			if (x.centers_user) != 0:
				if (x.centers_user*70>0.5):
					data_distance.append(x.centers_user*30)
				else:
					data_distance.append(x.centers_user*70)


		# Delete the distance metric object
		DistanceMetric.objects.all().delete()

	

		data = {
		        "labels": labels,
		        "default1": default_items,
		        "default2": default_items,

		        "default3": data_distance,


						}
		

		
		return Response(data)



# Create your views here.