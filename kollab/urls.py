from django.conf.urls import url
from kollab import views, apis

urlpatterns = [
	## for Views
	url(r'^$', views.index, name='index'),
#	url(r'^kollab/', include('kollab.urls')),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^login/$', views.login, name='login')
]