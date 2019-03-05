from django.conf.urls import url
from kollab import views, apis

urlpatterns = [
	## for Views
	url(r'^$', views.index, name='index'),
	
	## for processing REST api requests
	url(r'^submitSignUp/$', apis.signup, name='submitSignUp')
]