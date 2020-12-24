from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from profiles.models import Profile,Interest

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = [ 'username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = [ 'username','email']



class ProfileUpdateForm(forms.ModelForm):
    interest = forms.ModelMultipleChoiceField(
        queryset = Interest.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )
    contact_email = forms.EmailField(required=False)
    class Meta:
        model = Profile
        fields = ['profile_picture','bio','current_status','interest','contact_email']
    

