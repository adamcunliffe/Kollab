from django.contrib import admin
from kollab.models import Tag, UserProfile, Project, Membership

admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Membership)
