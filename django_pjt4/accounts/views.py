from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

# Create your views here.
def index(request):
    return render (request,'accounts/index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            new_user=form.save()
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            auth_login(request,authenticated_user)
            return redirect('accounts:profile', authenticated_user.username)
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/form.html',context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/form.html',context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:index')

@login_required
def profile(request,username):
    User = get_user_model()
    profile_user = User.objects.get(username=username)
    if len(str(profile_user.profile_picture)) == 0:
        profile_user.profile_picture = 'default_image.png'
        profile_user.save()
    context = {
        'profile_user' : profile_user,
    }

    return render(request,'accounts/profile.html',context)

@login_required
def follow(request,username):
    User = get_user_model()
    me = request.user
    you = User.objects.get(username=username)

    if me in you.followers.all():
        you.followers.remove(me)
    else:
        you.followers.add(me)

    return redirect('accounts:profile', username)