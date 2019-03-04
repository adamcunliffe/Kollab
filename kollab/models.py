from django.db import models

'''
kollab/models.py


How to use django.models : https://docs.djangoproject.com/en/2.1/ref/models/fields/

classes to be added:
	chat history
	API information which supports us using facebook, soundcloud apis etc
	


'''

class Tag(models.Model):
	# Might need to make each tage unique to ensure association between people via tags
	
	name = models.CharField(max_length=128)
	
	def __str__(self):
		return self.name

class User(models.Model):

	firstName = models.CharField(max_length=128)
	lastName = models.CharField(max_length=128)
	email = models.EmailField(null=True)
	
	# Users chosen location stored as latitude and longditude 
	# floatfield is just a decimal number like 50.938892 or -14.324333
	
	# stop these from being in the constructor!!
	lat = models.FloatField(blank=True)
	lon = models.FloatField(blank=True)
	
	''' to be added:
		portfolio --> one to one / one to many? --> portfolio class
		firstname and secondname
		search settings --> one to one --> search settings class
		
	'''
	
	# User has a many-to-many relationship with Tags becuase
	# tags are shared between users, (eg, musician tag can belong to two 
	# users) and users can have several tags
	tags = models.ManyToManyField(Tag)
	
	def __str__(self):
		return self.firstName + " " + self.lastName
		

		
class Project(models.Model):
	name = models.CharField(max_length=128)
	
	''' to be added:
		privacy setting - could be simple private/public or one to one link to a 
			project settings class
		projectAdmin --> one to many -->Admin
	'''
	
	# many to many for same reason as with person
	tags = models.ManyToManyField(Tag)
	
	# members is a list of Users
	members = models.ManyToManyField(User, through='Membership')
	
	def __str__(self):
		return self.name

class Membership(models.Model):
	# this sets a user as a member and ensures that if
	# the user is deleted from the project that they are not deleted 
	# from the database! blank = true ensures that when creating a new membership
	# that having a user/project is not a mandatory field
	user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
	project = models.ForeignKey(Project,models.SET_NULL, blank=True, null=True)
	
	''' to be added:
		date started membership / ended membership		
	'''
	def __str__(self):
		return self.user + ' ' + self.project