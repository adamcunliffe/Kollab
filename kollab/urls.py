from django.conf.urls import url
from kollab import views, apis

urlpatterns = [
	## for Views
	url(r'^$', views.index, name='index'),
#	url(r'^kollab/', include('kollab.urls')),
	
	url(r'^profile/(?P<user_name_slug>[\w\-]+)/$', views.profile, name='profile'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^login/$', views.login, name='login'),
	url(r'^collaborators/$', views.collaborators, name='collaborators')
	url(r'^collaborators/(?P<search_query>[\w\-]+)$', views.searchtags, name='searchtags')
]