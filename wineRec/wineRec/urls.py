"""wineRec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from search.views import *
from django.contrib.auth.views import login
#from django.contrib.auth.views import views as auth_views


urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^search/',include('search.urls')),
    #url(r'^$',index),
    #url(r'^login/$',auth_views.login),
    #url(r'^logout/$',auth_views.logout),

    #/person_list/80/
    #url(r'^person_details/(?P<person_id>[0-9]+)/$',person_details),
    #url(r'^display_wines/$',display_wine),
    #url(r'^login/$',login_view, {'template_name':'search/index.html'}),

]
