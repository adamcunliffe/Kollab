
#based on: https://www.diveinto.org/python3/your-first-python-program.html#importsearchpath
#anaconds search path is apparently incomplete?
import sys
sys.path.insert(0, 'D:\\Downloads\\Anaconda3\\envs\\kollab\\Lib\\site-packages')
sys.path.insert(0, 'D:\\PythonWorkspace\\kollab_project')

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kollab_project.settings')

import django
django.setup()
from kollab.models import User, Tag, Project, Membership

# Script which simulates typical data we need to save and retrieve

def populate():
	# data which will populate the database
	
	# seperate objects for music and film to seperate some users 
	# and create overlapping interests with other users
	music_tags = [
		{"name" : "Guitar"},
		{"name" : "Bass"} ]
	
	film_tags = [
		{"name" : "Film"},
		{"name" : "Cinematography"},
		{"name" : "Drama"}]
		
	all_tags = [music_tags, film_tags]	
	
		
	# website used to get lat lon: https://www.mapcoordinates.net/en
	# all lat lons refere to places around glasgow, starting from the centere & going out to dumbarton...dont know why I chose dumbarton...
	users = [
		{"name" : "Ananya",
		 "lat" : 55.84660244,
		 "lon" : -4.2240715 },
		 {"name" : "Barak",
		 "lat" : 55.87473302,
		 "lon" : -4.28724289 },
		 {"name" : "Charlie",
		 "lat" : 55.88407327,
		 "lon" : -4.33616638 },
		 {"name" : "David",
		 "lat" : 55.90794326,
		 "lon" : -4.40397263 },
		 {"name" : "Ebo",
		 "lat" : 55.86307864,
		 "lon" : -4.21926498 },
		 {"name" : "Faye",
		 "lat" : 55.92497052,
		 "lon" : -4.42337036 },
		 {"name" : "Genevieve",
		 "lat" : 55.94823863,
		 "lon" : -4.5658493 },
		 {"name" : "Haleigh",
		 "lat" : 55.97802448,
		 "lon" : -4.56550598 }]
	
	projects = [
		{"name": "documentory"},
		{"name": "indie band"},
		{"name": "drama film"}]
	
	preset_memberships_1 = [
		{"user" : users[0]},
		{"user" : users[5]},
		{"user" : users[2]} ]
		
	preset_memberships_2 = [
		{"user" : users[4]},
		{"user" : users[7]} ]
		
	preset_memberships_3 = [
		{"user" : users[6]},
		{"user" : users[1]} ]
		
	memberships = [
		preset_memberships_1,
		preset_memberships_2,
		preset_memberships_3 ]
	
	# iterating through data to functions
	
	for tag in all_tags:
		#print(tag)
		for t in tag:
			#print(t["name"])
			add_tag(t)
	
	for u in users:
		#print(u)
		add_user(u)
	
	for p in projects:
		#print(p)
		add_projects(p)
	
	# this loops through memberships and projects and feeds them
	# to add members
	# this loop assumes that the number of preset_membership == num of projects
	for index in range(0,len(projects)):
		for user in memberships[index]:
			add_members(projects[index]['name'], user['user']['name'])
	
	# this is a bit clunky but reflects the need to assign 
	# realistic tags to each project...
	
	# assign music tags to indie band and film tags to drama film
	
	# these loops are trying distribute the tags in a logical way, by theme, they are
	# very 'hacky' and will need to change as we develope the data set
	
	# note range is excluding documentories
	for index in range(1,len(projects)):
		for tag in all_tags[index-1]:
				print(tag)
				add_tags_to_project(projects[index], tag)
	
	## assign all tags to the documentory project (imagain its a doc about an indy band...to show collaboration / social networking etc)
	for tag in all_tags:
		for t in  tag:
			add_tags_to_project(projects[0], t)
	
	
	for project in Project.objects.all():
		members = project.members.all()
		tags = project.tags.all()
		print(project.name)
		if len(members) < len(tags):
			for tag in range(0, len(tags)):
				#modulo to distribute the tags among members
				index = tag % len(members)
				print(tags[tag])
				print(members[index])
				members[index].tags.add(Tag.objects.get(name = tags[tag]))
		else:
			for mem in range(0, len(members)):
				index = mem % len(tags)
				members[mem].tags.add(Tag.objects.get(name = tags[index]))
				
				
# functions for adding to database


def add_tag(tag):
	# seperating obj/created re docs: https://docs.djangoproject.com/en/2.1/ref/models/querysets/#get-or-create
	obj, created = Tag.objects.get_or_create(name=tag["name"])
	obj.save()
	
def add_user(user):
	obj, created = User.objects.get_or_create(name=user['name'], lon=user['lon'], lat=user['lat'])
	obj.save()
	
def add_projects(project):
	obj, created = Project.objects.get_or_create(name=project['name'])
	obj.save()
	
def add_members(proj, user):
	#print("add members:")
	#print(proj)
	#print(user)	
	obj, created = Membership.objects.get_or_create(user=User.objects.get(name=user), project=Project.objects.get(name=proj))
	obj.save()

def add_tags_to_project(proj, tag):
	#print(proj['name'] + "  " + tag['name'])
	project = Project.objects.get(name=proj['name'])
	obj, created = Tag.objects.get_or_create(name=tag['name'])
	obj.save()
	
	project.tags.add(obj)
		
if __name__ == '__main__':
	print("Starting Kollab population script...")
	populate()
		 