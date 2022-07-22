from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.models import User



# Create your views here.
"""
from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
        
        
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
        
        
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def my_view(request):
    ...
        
"""
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            
            
            if request.POST['username'] != None:
                username = request.POST['username']
                
            if request.POST['email'] != None:
                email = request.POST['email']
                username = User.objects.get(email=email)
                
            password = request.POST['password']    
            user = authenticate(request, username=username, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return HttpResponseRedirect(reverse('website:index'))
            else:
                messages.error(request, 'Username or password is incorrect')
                return HttpResponseRedirect(reverse('accounts:login'))
        else:
            return render(request,'accounts/login.html')
    return HttpResponseRedirect(reverse('website:index'))



def signup_view(request):
    return render(request,'accounts/signup.html')



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Successfully logged out')
        
    return HttpResponseRedirect(reverse('website:index'))