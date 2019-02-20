from django.conf.urls import url
from kollab import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
]