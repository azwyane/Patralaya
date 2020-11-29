from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect

#decorators for user follow
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# global decorator defined in common in root directory
from common.decorators import ajax_required


# contrib.auth User model
from django.contrib.auth.models import User

#local form 
from profiles.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

#function based paginator
from django.core.paginator import Paginator

#models
from profiles.models import Profile, Follow
from events.models import Bundle

# activity generation model utils
from activities.utils import create_action

def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            
            return render(request,'profiles/signup.html',{"form":form})    
    
    form = UserRegisterForm
    return render(request,'profiles/signup.html',{"form":form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"logged in as {username}")
                return redirect('home') 
            else:
                messages.error(request, "Invalid username or password.")
                
        else:
            for msg in form.error_messages:
                print(form.error_messages[msg])
            messages.error(request, "Invalid username or password.")
    
    form = AuthenticationForm()
    return render(request,'profiles/login.html',{"form":form})


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('home') 


def user_list(request):
    profile = Profile.objects.all
    return render(request,'profiles/profile_list.html',{'users': profile})
    

def user_detail(request,username):
    profile = get_object_or_404(Profile,user=User.objects.get(username=username))
    bundles = Bundle.objects.filter(creator=profile).order_by('-published_on')
    if (request.user.is_authenticated and 
        Profile.objects.get(user=request.user) 
            == Profile.objects.get(user=User.objects.get(username=username))):
        '''
        check if the requesting user is the owner of the bundle
        if True return all private and public bundle for the
        requesting user
        '''
        
        bundles = bundles.filter(
                    creator=Profile.objects.get(user=User.objects.get(username=username))
                    )
    else:
        '''
        if requesting user is not the owner of the bundle or
        is an anonymous user then return all public bundle
        of the provided username
        '''
        bundles = bundles.filter(
                creator=Profile.objects.get(user=User.objects.get(username=username)),
                status='Publish') 
    paginator = Paginator(bundles,3)
    page = request.GET.get('page')
    bundles = paginator.get_page(page)
    return render(request,'profiles/profile_detail.html',{'user': profile, 'bundles':bundles})


@login_required
def user_settings(request):
    if request.method == "POST":
        user_form = UserUpdateForm(
            request.POST,
            instance = request.user
            )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance = Profile.objects.get(user=request.user)
            )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect('home')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=Profile.objects.get(user=request.user))


    user_profile_forms = {
        'user_form':user_form,
        'profile_form':profile_form
    }

    return render(request,'profiles/settings.html',user_profile_forms)


@ajax_required
@require_POST
@login_required
def user_follow(request):
    profile_name = request.POST['username']
    action = request.POST['action']
    if profile_name and action:
        try:
            profile_to_follow = Profile.objects.get(
                user=User.objects.get(username=profile_name)
                )
            if action == 'follow':
                Follow.objects.get_or_create(
                    profile_from = Profile.objects.get(user=request.user),
                    profile_to = profile_to_follow
                    )
                create_action(Profile.objects.get(user=request.user), 'is following', profile_to_follow)
            else:
                Follow.objects.filter(
                    profile_from=Profile.objects.get(user=request.user),
                    profile_to=profile_to_follow
                    ).delete()
            
            return JsonResponse({'status':'ok'})
                
        except Profile.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})