from django.conf.urls import url
from kollab import views, apis

urlpatterns = [
    ## for Views
    url(r'^$', views.index, name='index'),
#    url(r'^kollab/', include('kollab.urls')),
    
    url(r'^profile/(?P<user_name_slug>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^project/(?P<project_name_slug>[\w\-]+)/$', views.project, name='project'),
	
    url(r'^firststep/$', views.login_register, name='login_register'),
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^login/authenticate/$', views.login_authenticate, name='login_authenticate'),
	
    url(r'^buildprofile/$', views.buildprofile, name='buildprofile'),
    url(r'^buildprofile/data/$', views.buildprofile_data, name='buildprofile_data'),
	
    url(r'^collaborators/$', views.collaborators, name='collaborators'),
    url(r'^collaborators/search/$', views.searchtags, name='searchtags'),
    url(r'^collaborators/search/(?P<tag_slug>[\w\-]+)/(?P<search_type>[\w\-]+)/$', views.embedded_search, name='embedded_search'),
	
	url(r'^logoff/$', views.logoff, name='logoff'),
	
	url(r'^collabs/respond/$', views.rest_collab_respond, name='collab_respond'),
]