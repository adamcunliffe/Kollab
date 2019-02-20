from django.db import models

'''
kollab/models.py


How to use django.models : https://docs.djangoproject.com/en/2.1/ref/models/fields/




'''

class Tag(models.Model):
	name = models.CharField(max_length=128)
	
	def __str__(self):
		return self.name

class User(models.Model):
	name = models.CharField(max_length=128)
	
	# Users chosen location stored as latitude and logditude 
	lat = models.FloatField()
	lon = models.FloatField()
	
	# User has a many-to-many relationship with Tags becuase
	# tags are shared between users, (eg, musician tag can belong to two 
	# users) and users can have several tags
	tags = models.ManyToManyField(Tag)
	
	def __str__(self):
		return self.name
		

		
class Project(models.Model):
	name = models.CharField(max_length=128)
	
	# many to many for same reason as with person
	tags = models.ManyToManyField(Tag)
	
	# members is a list of Users
	members = models.ManyToManyField(User, through='Membership')
	
	def __str__(self):
		return self.name

class Membership(models.Model):
	# this sets a user as a member and ensures that if
	# the user is deleted from the project that they are not deleted 
	# from the database! blank = true ensures that when creating a new projet
	# that having a user is not a mandatory field
	user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
	project = models.ForeignKey(Project,models.SET_NULL, blank=True, null=True)
	
	def __str__(self):
		return self.user + ' ' + self.project