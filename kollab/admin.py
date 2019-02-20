from django.contrib import admin
from kollab.models import Tag, User, Project, Membership

admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Membership)