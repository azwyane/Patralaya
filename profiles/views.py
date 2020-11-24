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
from profiles.forms import UserRegisterForm

#models
from profiles.models import Profile, Follow

def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home') #home view is the main page view for future

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
                return redirect('home') #home view is the main page view for future
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
    return redirect('home') #home view is the main page view for future


# @login_required
def user_list(request):
    profile = Profile.objects.all
    return render(request,'profiles/list.html',{'users': profile})
    
# @login_required
def user_detail(request,username):
    profile = get_object_or_404(Profile,user=User.objects.get(username=username))
    return render(request,'profiles/detail.html',{'user': profile})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    username = request.POST['username']
    action = request.POST['action']
    print(username,action)
    # if user_id and action:
    #     try:
    #         user = Profile.objects.get(user=User.objects.get(username=username))
    #         if action == 'follow':
    #             Follow.objects.get_or_create(
    #                 user_from=request.user,
    #                 user_to=user)
    #         else:
    #             Follow.objects.filter(user_from=request.user,user_to=user).delete()
            
    #         return JsonResponse({'status':'ok'})
                
    #     except User.DoesNotExist:
    #         return JsonResponse({'status':'error'})
    # return JsonResponse({'status':'error'})