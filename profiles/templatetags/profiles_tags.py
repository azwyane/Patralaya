from django import template
from ..models import Profile

register = template.Library()

@register.simple_tag
def profile_obj(user):
    return Profile.objects.get(user=user)