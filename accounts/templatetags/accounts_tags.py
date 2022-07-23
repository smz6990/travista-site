from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag(name='user_available')
def function(username):
    return not User.objects.filter(username=username).exists()
    