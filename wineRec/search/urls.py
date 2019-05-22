from django.conf.urls import url
from . import views
from .views import ChartData
from .views import HomeView, get_data, ChartData
app_name = 'search'
urlpatterns = [
	#url(r'^$',views.index,name='index'),

	url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^api/data/$', get_data, name='api-data'),
    url(r'^api/chart/data/$', ChartData.as_view()),



	url(r'^display_wines/',views.display_wine,name='display_wines'),
	url(r'^logout/',views.logout_view,name='logout'),
	url(r'^details/(?P<id>[0-9]+)/',views.wineDetails_view,name='details'),
	#url(r'^analysis/',views.statistical_analysis,name='statistical_analysis'),
	url(r'^charts/',ChartData.as_view()),
	#url(r'^(?P<wine>[0-9]+)/$',views.display_wine,name='display_wines'),



]