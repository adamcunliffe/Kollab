from django.shortcuts import render
from django.http import HttpResponse
	
def index(request):
	return render(request, 'kollab/index.html')
	
def login(request):
	return render(request, 'kollab/login.html')
	
def signup(request):
	return render(request, 'kollab/signup.html')