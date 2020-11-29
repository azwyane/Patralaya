from django import template
from ..models import Profile

register = template.Library()

@register.simple_tag
def profile_obj(user):
    return Profile.objects.get(user=user)

@register.simple_tag
def profile_followings(user):
    return Profile.objects.filter(followers=user).all()