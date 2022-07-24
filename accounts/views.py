from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password,password_changed
from accounts.forms import NewUserFrom

def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['username']
            password = request.POST['password']
            # check for email
            if '@' in name:
                try:
                    username = User.objects.get(email=name)
                except:
                    messages.error(request, 'Invalid username\email or password')
                    return HttpResponseRedirect(reverse('accounts:login'))
            else:
                username = request.POST['username']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f'Welcome back {username}')
                return HttpResponseRedirect(reverse('website:index'))
            else:
                messages.error(request,'Invalid username\email or password')
        
        return render(request,'accounts/login.html')
    return HttpResponseRedirect(reverse('website:index'))


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = NewUserFrom(request.POST)
            if form.is_valid():
                user = form.save()
                login(request,user)
                messages.success(request,'User created successfully')
                messages.success(request,f'Welcome {user.username}')
                return HttpResponseRedirect(reverse('website:index'))
            messages.error(request,'Invalid information')
            messages.error(request,form.errors)
        form = NewUserFrom()
        context = {
            'form':form
            }
        return render(request,'accounts/signup.html',context)
    return HttpResponseRedirect(reverse('website:index'))
    
    
    
@login_required(redirect_field_name='/')
def logout_view(request):
 
    logout(request)
    messages.info(request, 'Successfully logged out')      
    return HttpResponseRedirect(reverse('website:index'))


def reset_password_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request,"Username is incorrect")
                return HttpResponseRedirect(reverse('accounts:resetpassword'))
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            
            if (user is not None) and (user.email == email) and (password1==password2):
                try:
                    validate_password(password=password1,user=username)
                except:
                    messages.error(request,"Passwords didn't match")
                    return HttpResponseRedirect(reverse('accounts:resetpassword'))
                else:
                    user.set_password(password1)
                    user.save()
                    password_changed(password=password1,user=user)
                    login(request,user)
                    messages.success(request,"Password successfully changed")
                    return HttpResponseRedirect(reverse('website:index'))                

            else:
                messages.error(request,'Inputs are incorrect')
                return HttpResponseRedirect(reverse('accounts:resetpassword'))
                
        else:
            return render(request,'accounts/reset-password.html')
    else:
        return HttpResponseRedirect(reverse('website:index'))
