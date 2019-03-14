from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from kollab.forms import UserForm, UserProfileForm
from kollab.models import Tag, UserProfile, Membership, Project
from django.core.exceptions import ObjectDoesNotExist
import re


def index(request):
    return render(request, 'kollab/index.html')


def login(request):
    return render(request, 'kollab/login.html')

def firststep(request):

    if request.method == 'POST':
        username = request['username']
        email = request['user-email']
        password1 = request['user-pass']
        password2 = request['user-repeatpass']
# need a check here, possibly javascript, to see whether passwords match

        # if username == '' or password == '':
        #     return render('login.html', {'form_error': 'The passwords do not match'})

        user = User(username=username, password=password1, email=email)
        user.save()

        return render(request, 'kollab/login,html')


def secondstep(request):

    if request.method == 'POST':
        firstName = request['firstName']
        lastName = request['lastName']

# def step2():
#     if post
#         profile = UserProfile()
#         profile.user = logged in


# def signup(request):
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#
#             user.set_password(user.password)
#             user.save()
#
#             profile1 = profile_form.save(commit=False)
#             profile1.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile1.save()
#
#             registered = True
#
#         else:
#             print(user_form.errors, profile_form.errors)
#
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#             # username = form.cleaned_data.get('username')
#             # raw_password = form.cleaned_data.get('password')
#             # email = form.cleaned_data.get('email')
#             # user = authenticate(username=username, password=raw_password)
#             # login(request, user)
#             # return redirect('home')
#
#     return render(request, 'kollab/signup.html', {'user_form': user_form,
#                                                   'profile_form': profile_form,
#                                                   'registered': registered})
    
    
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
    
def project(request, project_name_slug):
    context = {}
    try:
       projprof = Project.objects.get(slug=project_name_slug)
    except ObjectDoesNotExist:
       return HttpResponse("Does not exist...temp error page")
    
    context['name'] = projprof.name
    context['short'] = projprof.short
    context['long'] = projprof.long
    context['picture'] = projprof.picture
    context['members'] = projprof.members
    
    tags = projprof.tags.all()
    tagset = set()
    for t in tags.all():
        tagset.add(t.name)
        
    context['tags'] = tagset
      
    return render(request, 'kollab/project.html', context)
    
def collaborators(request):
    return render(request, 'kollab/collaborators.html')
    

def searchtags(request):
    context = {}
    if request.method == 'POST':
        raw_query = request.POST.get('search_query', None)
        search_option = request.POST.get('search_option', None)
        search_query = clean(raw_query.lower())
        query_tags, context['error_message'] = removeUseless(search_query)
        
        if search_option != "Projects":
            context['results'] = get_user_results(query_tags)
            context['type'] = 'users'
        else:
            context['results'] = get_project_results(query_tags)
            context['type'] = 'projects'
        
        
        print(search_query)
        
        print(query_tags, context['error_message'])
        
        
        return render(request, 'kollab/collaborators.html', context)
    else:
        print('not a post!')
        context['error_message'] = "Sorry, but the system has failed to search"
    return render(request, 'kollab/collaborators.html', context)
    
def embedded_search(request, tag_slug, search_type):
    context = {}
    
    query_tags = []
    
    query_tags.append(tag_slug.lower())
    
    if search_type != "project":
        context['results'] = get_user_results(query_tags)
        context['type'] = 'users'
    else:
        context['results'] = get_project_results(query_tags)
        context['type'] = 'projects'
    
        
    print(query_tags, context['results'])
    
    
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
    
def get_project_results(query_tags):
    results = Project.objects.none()
    for i in range(0, len(query_tags)):
        if 'Not Valid' not in query_tags[i]:
            query = Project.objects.filter(tags__name__contains=query_tags[i])
            results = results | query
            
    print(results.distinct())
    return results.distinct();