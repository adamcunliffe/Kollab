# based on: https://www.diveinto.org/python3/your-first-python-program.html#importsearchpath
# anaconds search path is apparently incomplete?

# If you are having trouble importing django then fill in and include the below script:
# import sys
# sys.path.insert(0, 'PATH_TO_ANACONDA\\Anaconda3\\envs\\kollab\\Lib\\site-packages')
# sys.path.insert(0, 'PATH_TO_YOUR_PYHON_WORKSPACE\\PythonWorkspace\\kollab_project')

import sys

sys.path.insert(0, 'D:\\Downloads\\Anaconda3\\envs\\kollab\\Lib\\site-packages')
sys.path.insert(0, 'D:\\PythonWorkspace\\PythonWorkspace\\kollab_project')

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kollab_project.settings')

import django

django.setup()
from django.contrib.auth.models import User
from kollab.models import UserProfile, Tag, Project, Membership, Collabs
from django.core.files import File
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
import random
from django.contrib.auth.hashers import make_password


# Script which simulates typical data we need to save and retrieve

def populate():
    # data which will populate the database

    # seperate objects for music and film to seperate some users 
    # and create overlapping interests with other users
    music_tags = [
        {"name": "Guitar"},
        {"name": "Bass"}]

    film_tags = [
        {"name": "Film"},
        {"name": "Cinematography"},
        {"name": "Drama"}]

    all_tags = [music_tags, film_tags]

    ## generic lorum ipsum style text...in the fashion of Bob Ross

    stringananya = "Hi, my name is Ananya! I'm a cat loving guitarist and film student from Glasgow, Scotland" \
                   "I'm hoping to find some local film-makers or actors to help collaborate on my final year project." \
                   "Fans of horror films - let me know!"

    stringbarak = "I'm Barak and I live to play guitar. I live in Edinburgh, so if any local fans of indie/rock music" \
                  "want to start a band - let me know! I'm also a fan of acting, so if anyone needs any part-time" \
                  "actors for fun projects, I'd love to help."

    stringcharlie = "The name is Charlie, and I'm an actor from London. I travel a lot, so I'm happy to collaborate" \
                    "on projects across the UK. I have been acting for 15 years and would love to be part of a few" \
                    "experimental films."

    stringdav = "I'm Dav, and I love to paint and make art. If anyone in Scotland wants to work on some big murals," \
                "I'd love to be a part of that."

    stringebo = "I'm Ebony or Ebo for short. I'm a musician, specifically a guitarist, and would love to work with " \
                "some local musicians on some folk projects. Influences include Bob Dylan, The Avett Brothers," \
                "Mumford & Sons and NWA"

    stringfaye = "Heyyyy, I'm Fayeeeeee. I'm a bass player from Scotland who lives and breathes METAL. Applicants" \
                 " must love Metallica, Mastodon and nights out at Catty. Let's start a band!"

    stringgerry = "My name is Gerry. I'm a 50 year old cinematographer with over 25 years in the business. Drop me " \
                  "a message if you have any interesting visual projects in mind."

    stringharry = "I'm Harry and I like the bass. Looking to start a rock band in Glaasgow! Influences include" \
                  "The Strokes, The Killers and Radiohead."


    # website used to get lat lon: https://www.mapcoordinates.net/en
    # all lat lons refer to places around glasgow, starting from the center

    '''users = [
        {"username" : "Ananya",
         "email": "Ananya@ex.com",
         "password" : "predictable"},
         {"username" : "Barak",
         "email": "Barak@ex.com",
         "password" : "predictable"},
         {"username" : "Charlie",
         "email": "Charlie@ex.com",
         "password" : "predictable"},
         {"username" : "Dav",
         "email": "Dav@ex.com",
         "password" : "predictable"},
         {"username" : "Ebo",
         "email": "Ebo@ex.com",
         "password" : "predictable"},
         {"username" : "Faye",
         "email": "Faye@ex.com",
         "password" : "predictable"},
         {"username" : "Gerry",
         "email": "Gerry@ex.com",
         "password" : "predictable"},
         {"username" : "Harry",
         "email": "Harry@ex.com",
         "password" : "predictable"}]'''

    hashedPassword = make_password("predictable", salt=None, hasher='default')
    # need to give users proper first and last names
    users = [
        {"username": "Ananya",
         "email": "Ananya@ex.com",
         "password": hashedPassword},
        {"username": "Barak",
         "email": "Barak@ex.com",
         "password": hashedPassword},
        {"username": "Charlie",
         "email": "Charlie@ex.com",
         "password": hashedPassword},
        {"username": "Dav",
         "email": "Dav@ex.com",
         "password": hashedPassword},
        {"username": "Ebo",
         "email": "Ebo@ex.com",
         "password": hashedPassword},
        {"username": "Faye",
         "email": "Faye@ex.com",
         "password": hashedPassword},
        {"username": "Gerry",
         "email": "Gerry@ex.com",
         "password": hashedPassword},
        {"username": "Harry",
         "email": "Harry@ex.com",
         "password": hashedPassword}]

    userProfiles = [
        {"selfinfo": stringananya,
         "picture": "static/images/ananya.jpg",
         "lat": 55.87473302,
         "lon": -4.28724289},
        {"selfinfo": stringbarak,
         "picture": "static/images/barak.jpg",
         "lat": 55.879151,
         "lon": -4.297939},
        {"selfinfo": stringcharlie,
         "picture": "static/images/charlie.jpg",
         "lat": 55.892919,
         "lon": -4.252720},
        {"selfinfo": stringdav,
         "picture": "static/images/dav.jpg",
         "lat": 55.816863,
         "lon": -4.088308},
        {"selfinfo": stringebo,
         "picture": "static/images/ebo.jpg",
         "lat": 55.826564,
         "lon": -4.255632},
        {"selfinfo": stringfaye,
         "picture": "static/images/faye.jpg",
         "lat": 55.860551,
         "lon": -4.244649},
        {"selfinfo": stringgerry,
         "picture": "static/images/gerry.jpg",
         "lat": 55.894544,
         "lon": -4.058033},
        {"selfinfo": stringharry,
         "picture": "static/images/harry.jpg",
         "lat": 55.845072,
         "lon": -4.426978}]

    projects = [
        {"name": "Magic Music",
         "picture": "static/images/pexels-photo-1120162.jpg",
         "short": "Music documentary from Glasgow",
         "long": "We're making a documentary about the local music scene in Glasgow! Calling all film makers, musicians"
                 "and artists!"},
        {"name": "Weegie Funk Legends",
         "picture": "static/images/pexels-photo-1813124.jpg",
         "short": "Fusion // Low-Fi // Weegie-Wave",
         "long": "We're the Weegie Funk Legends. A 4-piece from Glasgow. Rocking your face off since 2018."},
        {"name": "Taming of the Shew",
         "picture": "static/images/pexels-photo-1049746.jpg",
         "short": "Glasgow Youth Theater",
         "long": "Glasgow Youth Theater is putting on a performance of William Shakespeare's The Taming of the Shrew"}]

    preset_memberships_1 = [
        {"user": users[0]},
        {"user": users[5]},
        {"user": users[2]},
        {"user": users[7]}]

    preset_memberships_2 = [
        {"user": users[4]},
        {"user": users[7]},
        {"user": users[1]}]

    preset_memberships_3 = [
        {"user": users[0]},
        {"user": users[6]},
        {"user": users[1]}]

    memberships = [
        preset_memberships_1,
        preset_memberships_2,
        preset_memberships_3]

    preset_collabs_1 = [
        users[0],
        users[4],
        users[5]]

    preset_collabs_2 = [
        users[1],
        users[6],
        users[7],
        users[4],
        users[5], ]

    preset_collabs_3 = [
        users[2],
        users[4],
        users[5]]

    preset_collabs_4 = [
        users[3],
        users[4],
        users[5],
        users[6], ]

    collabs = [
        preset_collabs_1,
        preset_collabs_2,
        preset_collabs_3,
        preset_collabs_4]

    # iterating through data to functions

    for tag in all_tags:
        # print(tag)
        for t in tag:
            # print(t["name"])
            add_tag(t)

    for i in range(0, len(users)):
        # print(u)
        add_user(users[i], userProfiles[i])

    for p in projects:
        # print(p)
        add_projects(p)

    # this loops through memberships and projects and feeds them
    # to add members
    # this loop assumes that the number of preset_membership == num of projects
    for index in range(0, len(projects)):
        for user in memberships[index]:
            add_members(projects[index]['name'], user['user'])

    # this is a bit clunky but reflects the need to assign 
    # realistic tags to each project...

    # assign music tags to indie band and film tags to drama film

    # these loops are trying distribute the tags in a logical way, by theme, they are
    # very 'hacky' and will need to change as we develope the data set

    # note range is excluding documentories
    for index in range(1, len(projects)):
        for tag in all_tags[index - 1]:
            print(tag)
            add_tags_to_project(projects[index], tag)

    ## assign all tags to the documentory project (imagain its a doc about an indy band...to show collaboration / social networking etc)
    for tag in all_tags:
        for t in tag:
            add_tags_to_project(projects[0], t)

    for project in Project.objects.all():
        members = project.members.all()
        tags = project.tags.all()
        print(project.name)
        if len(members) < len(tags):
            for tag in range(0, len(tags)):
                # modulo to distribute the tags among members when mem > tags
                index = tag % len(members)
                print(tags[tag])
                print(members[index])
                members[index].tags.add(Tag.objects.filter(name=tags[tag]).first())
        else:
            for mem in range(0, len(members)):
                index = mem % len(tags)
                members[mem].tags.add(Tag.objects.filter(name=tags[index]).first())

    # adds Collabs (friends) an randomly sets them to sent or confirmed setting for testing
    for i in range(0, len(collabs)):
        preset_collab = collabs[i]
        collab_adder = preset_collab[0]
        print("add collabs " + collab_adder['username'])
        user = User.objects.get(username=collab_adder['username'])
        adder_userprof = UserProfile.objects.get(user=user)

        # now go through the rest of the list and create an instance of Collabs for each initiated by the adder_userprof
        for j in range(1, len(preset_collab)):
            recipiant = preset_collab[j]
            user = User.objects.get(username=recipiant['username'])
            recip_userprof = UserProfile.objects.get(user=user)

            if not adder_userprof.collabs_recieved.filter(creator=recip_userprof).exists():
                if random.randint(0, 1) == 1:
                    state = Collabs.SENT
                else:
                    state = Collabs.CONFIRMED
                print(
                    "collab attempted (success): " + adder_userprof.user.username + " " + recip_userprof.user.username)
                col, created = Collabs.objects.get_or_create(creator=adder_userprof, friend=recip_userprof,
                                                             status=state)
                col.save()
            else:
                print("collab attempted (fail): " + adder_userprof + " " + recip_userprof)


# functions for adding to database


def add_tag(tag):
    # seperating obj/created re docs: https://docs.djangoproject.com/en/2.1/ref/models/querysets/#get-or-create
    obj, created = Tag.objects.get_or_create(name=tag["name"])
    obj.save()


# may raise an integrity error if trying to get user thats already been added, just remove them from the data base
def add_user(user, userProfile):
    # obj, created = User.objects.get_or_create(firstName=user['firstName'], lastName=user['lastName'], email=user['email'],lon=user['lon'], lat=user['lat'])
    newuser, created = User.objects.get_or_create(username=user['username'], email=user['email'],
                                                  password=user['password'])
    newuser.save()
    profile, created = UserProfile.objects.get_or_create(user=newuser)
    profile.firstname = user['username']
    profile.lastname = "Test" + str(random.randint(1, 100))
    profile.lat = userProfile['lat']
    profile.lon = userProfile['lon']
    profile.selfinfo = userProfile['selfinfo']
    profile.picture = File(open(userProfile['picture'], 'rb'))
    profile.save()


def add_projects(project):
    obj, created = Project.objects.get_or_create(name=project['name'], short=project['short'], long=project['long'])
    try:
        obj.picture = File(open(project['picture'], 'rb'))
    except Exception:
        print("error")
    obj.save()


def add_members(proj, user):
    # print("add members:")
    # print(proj)
    # print(user)    # this = UserProfile.objects.get(user=(User.objects.get(username="test1")))
    obj, created = Membership.objects.get_or_create(
        userProfile=UserProfile.objects.get(user=User.objects.get(username=user['username'])),
        project=Project.objects.get(name=proj))
    obj.save()


def add_tags_to_project(proj, tag):
    # print(proj['name'] + "  " + tag['name'])
    project = Project.objects.get(name=proj['name'])
    obj, created = Tag.objects.get_or_create(name=tag['name'])
    obj.save()

    project.tags.add(obj)


if __name__ == '__main__':
    print("Starting Kollab population script...")
    populate()
