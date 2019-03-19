from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from kollab.forms import UserForm, UserProfileForm
from kollab.models import Tag, UserProfile, Membership, Project, Collabs
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import re


def index(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'kollab/index.html', context=context_dict)
    return response


def login_page(request):
    if request.session.test_cookie_worked(): 
        print("TEST COOKIE WORKED!") 
        request.session.delete_test_cookie()
        
    context = {}
    context['click'] = "=false"
    return render(request, 'kollab/login.html', context)
    
def login_authenticate(request):
    context = {}
    if request.method == 'POST':
       email = request.POST.get('email', None)
       password = request.POST.get('password', None)
       
       try:
           user = User.objects.get(email=email)
       except ObjectDoesNotExist:
           context['loginerror'] = "=true"
           return render(request, 'kollab/login.html', context)
           print('error!')
           
       logged_user = authenticate(username=user.username, password=password)
       print(email + "  " + password) 
       
       if logged_user is not None:
           login(request, logged_user)
           print('got to login')           
           prof = UserProfile.objects.get(user=logged_user)
           # temporary redirect to build profile, should probibly be collabprate / logged_user profile
           return HttpResponseRedirect(reverse('profile', kwargs={'user_name_slug': prof.slug}))
       else:
           context['loginerror'] = "=true"
       print('login failed')
       return render(request, 'kollab/login.html', context)
        

def login_register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('user-email', None)
        password1 = request.POST.get('user-pass', None)
        password2 = request.POST.get('user-repeatpass', None)
        
        isValid = True;
        error = []
        if User.objects.filter(username=username).exists():
            error.append("Username <strong>" + username + "</strong> already exists.")
            isValid = False
            
        if User.objects.filter(email=email).exists():
            error.append("Email <strong>" + email + "</strong> already exists.")
            isValid = False
            
        if password1 != password2:
            error.append( "Passwords were not identical.")
            isValid = False
            
        
        
        if isValid:
            user = User.objects.create_user(username=username, password=password1, email=email)
            user.save()
            user = authenticate(request, username=username, password=password1)
            print("user: "+ user.username)
            if user is not None:
                login(request, user)
            return HttpResponseRedirect(reverse('buildprofile'))

        if not isValid: 
            context['error'] = error
            context['click'] = "=true"
            return render(request, 'kollab/login.html', context)
        
        
def logoff(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def secondstep(request):

    if request.method == 'POST':
        firstName = request['firstName']
        lastName = request['lastName']

@login_required        
def buildprofile(request):
    context = {}
    
    loc_user = request.user #User.objects.get(username="test5")
        
    user_query = UserProfile.objects.filter(user=loc_user)
    
    user = user_query[0]
    
    if user is not None:    
        context['picture'] = user.picture
        context['firstname'] = user.firstname
        context['lastname'] = user.lastname
        context['selfinfo'] = "I like to... \n\n\n I am interested in..."
    else:
        context['picture'] = "/default-profile.jpg"
        context['firstname'] = "Andrew"
        context['lastname'] = "Smith"
        context['selfinfo'] = "I like to... \n\n\n I am interested in..."
    
    return render(request, 'kollab/buildprofile.html', context)

@login_required
def buildprofile_data(request):
    if request.method == 'POST':
        tags = request.POST.getlist('tags', '')
        #tag_string = request.POST.get('tag-string', '')
        print(tags)
        
        if request.POST.get('tag-string', '') is not "":
            if tags is not "":
                tags += clean(request.POST.get('tag-string', ''))
            else:
                tags = clean(request.POST.get('tag-string', ''))
        
        print(tags)
        
        pic = request.POST.get('profile-pic','')
        print(pic)
        
        print_post(request)
        
        loc_user = request.user #User.objects.get(username="test5")
        form = {}
        
        prof, created = UserProfile.objects.get_or_create(user=loc_user)        
        
        if request.POST.get('firstName','') is not "":
            prof.firstname = request.POST.get('firstName','')
            
        if request.POST.get('lastName','') is not "":
            prof.lastname = request.POST.get('lastName','')
            
        if request.FILES.get('profile-pic', '') is not "":
            prof.picture = request.FILES.get('profile-pic', '')
            
        if request.POST.get('selfinfo','') is not "":
            prof.selfinfo = request.POST.get('selfinfo','')
            
        print(prof.firstname)
        prof.save()
        
        # reset tags
        
        if tags is not "":        
            prof.tags.clear()
            
            for i in range(0, len(tags)):
                if Tag.objects.filter(name=tags[i].lower()).exists():
                    tag = Tag.objects.filter(name=tags[i].lower()).first()
                    print(tag)
                else:
                    tag = Tag.objects.create(name=tags[i])
                    print(tag)
                tag.save()
                
                prof.tags.add(tag)
        
        prof.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'user_name_slug': prof.slug}))
    
    return HttpResponse("big ass error")
    

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
    
@login_required
def profile(request, user_name_slug):
    context = {}
    print(user_name_slug)
    #user = User.objects.get(username=user_name_slug)
    #print(user.email)
    try:
       userprof = UserProfile.objects.get(slug=user_name_slug)
    except ObjectDoesNotExist:
       return HttpResponse("Does not exist...temp error page")
    
    current_user = UserProfile.objects.get(user=request.user)
    
    #context['collabsconfirmed'] = current_user.collabs_initiated.filter(status=Collabs.CONFIRMED) | current_user.collabs_recieved.filter(status=Collabs.CONFIRMED)
   # context['current_user'] = current_user
   
    context = get_user_sidebar_info(request)
   
    context['currentuserslug'] = current_user.slug
    context['profileslug'] = user_name_slug
    context['username'] = userprof.user.username
    context['firstname'] = userprof.firstname
    context['lastname'] = userprof.lastname
    context['location'] = "Exampleton"
    context['latlon'] = [userprof.lat, userprof.lon]
    context['picture'] = userprof.picture
    context['selfinfo'] = userprof.selfinfo
    context['tags'] = userprof.tags.all()
    context['collaborations'] = Membership.objects.filter(userProfile = UserProfile.objects.get(slug=user_name_slug))
    
    # if they already have a collab relationship, get status
    
    collab = get_first_collabs(userprof, current_user)
    if collab is None:
        context['hascollab'] = "=false"
    else: 
        context['hascollab'] = "=true"
        context['collabstatus'] =  collab.status
    
    
    if current_user.slug == user_name_slug:
        return personal_profile(request, context, current_user)
    
    return render(request, 'kollab/profile-general.html', context)

# Method that supports Views.profile to display to the current user
@login_required    
def personal_profile(request, context, current_user):
    print('success')
    context['currentuser'] = current_user.user.username
    
   
    context['collabssent'] = current_user.collabs_initiated.filter(status=Collabs.SENT)
    context['collabsrecieved'] = current_user.collabs_recieved.filter(status=Collabs.SENT)
    context['collabsdenied'] = current_user.collabs_initiated.filter(status=Collabs.DENIED) | current_user.collabs_recieved.filter(status=Collabs.DENIED)
    context['collabsconfirmed'] = current_user.collabs_initiated.filter(status=Collabs.CONFIRMED) | current_user.collabs_recieved.filter(status=Collabs.CONFIRMED)
    
    print(context['collabsconfirmed'].values())
    
    return render(request, 'kollab/profile-personal.html', context)
    
@login_required
def rest_collab_respond(request):
    print('respond ')
    print_post(request)
    list = request.POST.getlist('collab-sender-username')
    reciever_profile = UserProfile.objects.get(user=request.user)
    
    for i in range(0, len(list)):
        print(list[i])
        sender_profile = UserProfile.objects.get(slug=list[i])
        responsestring = request.POST.get('options-'+list[i])
        
        # if there is no response for this sender then skip this loop
        if responsestring is None:
            continue
            
        #going to get an instance of a collab, make sure we get the right one!
        #use helper function to single out only the first on based on date time, a messy way of keeping it consistant
        collab = get_first_collabs(reciever_profile, sender_profile)
        
        status = get_collabs_status(responsestring)
        
        if status is not None: 
            print("status: " + status)
            collab.status = status
            collab.save()
        else:
            print("Error confirming collabs status...check form string")
            
        #might want to take this chance to search for and remove/edit any that are going the other way
        print("To " + reciever_profile.slug + " sender " + sender_profile.slug + " response " + responsestring)
    
    return HttpResponse("success")

@login_required
def rest_collab_initiate(request):
    print('respond ')
    for key, values in request.POST.lists():
        print(key, values)
        
    creator = UserProfile.objects.get(slug=request.POST.get('collab-creator-username'))
    recipient = UserProfile.objects.get(slug=request.POST.get('collab-recipient-username'))
    
    collabs = Collabs.objects.create(creator=creator, friend=recipient, status=Collabs.SENT)
    collabs.save()
    
    prior = collabs.id
    
    print("prior to get first " + str(collabs.id))
    
    collabs = get_first_collabs(recipient, creator)
    after = collabs.id
    print("after get first " + str(collabs.id))
    
    if prior == after:
        print("New - collab with status: " + collabs.status)
    else:
        print("Old - collab with status: " + collabs.status)
    
    return HttpResponse('success')
 
#helper function for getting the first collabs request between to users
def get_first_collabs(reciever_profile, sender_profile):
    co1 = Collabs.objects.filter(creator=reciever_profile, friend=sender_profile)
    co2 = Collabs.objects.filter(creator=sender_profile, friend=reciever_profile)
    
    all = co1 | co2    
    first = all.order_by('created').first()
    
    # this deletes all others apart from first, which was the first created collabs request
    '''extra = all.exclude(id=first.id)
    extra.delete()'''
    
    return first
    
# helper function for returning the Model.Collabs status string
def get_collabs_status(responsestring):
    if "sent" in responsestring.lower():
        return Collabs.SENT
    elif "conf" in responsestring.lower():
        return Collabs.CONFIRMED
    elif "den" in responsestring.lower():
        return Collabs.DENIED
    else:
        return None

 
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
    context = get_user_sidebar_info(request)
    return render(request, 'kollab/collaborators.html', context)

def chat(request):
    context = get_user_sidebar_info(request)
    return render(request, 'kollab/chat.html', context)

@login_required
def searchtags(request):
    context = {}
    context = get_user_sidebar_info(request)
    
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
 
@login_required
def embedded_search(request, tag_slug, search_type):
    context = {}
    context = get_user_sidebar_info(request)
    
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
    
# Helper method to return sidebar information
def get_user_sidebar_info(request):
    context = {}
    current_user = UserProfile.objects.get(user=request.user)
    context['collabsconfirmed'] = current_user.collabs_initiated.filter(status=Collabs.CONFIRMED) | current_user.collabs_recieved.filter(status=Collabs.CONFIRMED)
    context['current_user'] = current_user
    
    return context
  
 # Helper method to print post requests
def print_post(request):
    for key, values in request.POST.lists():
        print(key, values)

# remove everything that is not a letter or regular space, return array
def clean(raw_query):
    return re.sub('[^a-zA-Z ]', "", raw_query).split(" ")
 
#helper functions for the search
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

    
# A helper method for cookies
def get_server_side_cookie(request, cookie, default_val=None): 
    val = request.session.get(cookie) 
    if not val: 
        val = default_val 
    return val


def visitor_cookie_handler(request): 
    # Get the number of visits to the site. 
    # We use the COOKIES.get() function to obtain the visits cookie. 
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used. 
    visits = int(get_server_side_cookie(request, 'visits', '1')) 
    last_visit_cookie = get_server_side_cookie(request, 
                                               'last_visit', 
                                               str(datetime.now()))  
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], 
                                        '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit... 
    if (datetime.now() - last_visit_time).days > 0: 
        visits = visits + 1 
        # Update the last visit cookie now that we have updated the count 
        request.session['last_visit'] = str(datetime.now())



    else: 
        # Set the last visit cookie 
        request.session['last_visit'] = last_visit_cookie

        # Update/set the visits cookie 
        request.session['visits'] = visits

