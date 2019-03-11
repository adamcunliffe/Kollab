from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
##from kollab.forms import SignUpForm
from kollab.models import Tag, UserProfile, Membership
from django.core.exceptions import ObjectDoesNotExist
import re


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
    
    
def profile(request, user_name_slug):
    context = {}
    print(user_name_slug)
    #user = User.objects.get(username=user_name_slug)
    #print(user.email)
    try:
       userprof = UserProfile.objects.get(slug=user_name_slug)
    except ObjectDoesNotExist:
       return HttpResponse("Does not exist...temp error page")
    
    context['firstName'] = userprof.user.username
    context['secondName'] = ""
    context['location'] = "Exampleton"
    context['latlon'] = [userprof.lat, userprof.lon]
    context['picture'] = userprof.picture
    context['selfinfo'] = userprof.selfinfo
    context['tags'] = userprof.tags.all()
    context['collaborations'] = Membership.objects.filter(userProfile = UserProfile.objects.get(slug=user_name_slug))
    
    return render(request, 'kollab/profile.html', context)
    
def collaborators(request):
    return render(request, 'kollab/collaborators.html')
    

def searchtags(request):
    context = {}
    if request.method == 'POST':
        raw_query = request.POST.get('search_query', None)
        search_query = clean(raw_query.lower())
        print(search_query)
        query_tags, context['error_message'] = removeUseless(search_query)
        print(query_tags, context['error_message'])
        context['results'] = get_user_results(query_tags)
        
        return render(request, 'kollab/collaborators.html', context)
    else:
        print('not a post!')
        context['error_message'] = "Sorry, but the system has failed to search"
    return render(request, 'kollab/collaborators.html', context)

# remove everything that is not a letter or regular space, return array
def clean(raw_query):
    return re.sub('[^a-zA-Z ]', "", raw_query).split(" ")
   
#remove tags that dont exist
def removeUseless(search_query):
    error = ""
    for i in range(0, len(search_query)):
        if not Tag.objects.filter(name__contains=search_query[i]).exists():
            error += search_query[i] + " "
            search_query[i] = "Not Valid"
        else:
            print(search_query[i])
        
    return search_query, error;
    
def get_user_results(query_tags):
    results = UserProfile.objects.none()
    for i in range(0, len(query_tags)):
        if 'Not Valid' not in query_tags[i]:
            query = UserProfile.objects.filter(tags__name__contains=query_tags[i])
            results = results | query
            
    print(results.distinct())
    return results.distinct();
