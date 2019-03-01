import os
from django import template
from django.conf import settings


register = template.Library()

@register.simple_tag
def bootstrap():
	return os.path.join(settings.BASE_DIR, 'static/bootstrap/')