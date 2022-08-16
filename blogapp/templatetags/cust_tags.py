from django import template
from django.contrib.auth.models import User

register = template.Library()
@register.simple_tag
def users_list():
    users_list=User.objects.all()
    return users_list