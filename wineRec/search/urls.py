from django.conf.urls import url
from . import views


app_name = 'search'
urlpatterns = [
	#url(r'^$',views.index,name='index'),
	url(r'^display_wines/',views.display_wine,name='display_wines'),
	url(r'^logout/',views.logout_view,name='logout'),
	url(r'^details/(?P<id>[0-9]+)/',views.wineDetails_view,name='details'),
	#url(r'^(?P<wine>[0-9]+)/$',views.display_wine,name='display_wines'),



]