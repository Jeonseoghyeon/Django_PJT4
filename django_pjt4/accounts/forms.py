from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name','email','profile_picture']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['profile_picture']