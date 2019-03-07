from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from kollab.forms import SignUpForm
from kollab.models import UserProfile


def index(request):
    return render(request, 'kollab/index.html')


def login(request):
    return render(request, 'kollab/login.html')


def signup(request):
    return render(request, 'kollab/signup.html')


def signup(request):
    if request.method == 'POST':
        form = signup(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'kollab/signup.html', {'form': form})