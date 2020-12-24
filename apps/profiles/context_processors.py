from profiles.models import Profile

def profile_render(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {
            'user_profile':profile
        }
    else:
        return {
            'user_profile':''
        }