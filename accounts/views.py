from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password,password_changed



def login_view(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST': 
            password = request.POST['password']    
            
            name = request.POST['username']
            if '@' in name:
                try:
                    username = User.objects.get(email=name)
                except:
                    messages.error(request, 'Email is incorrect')
                    return HttpResponseRedirect(reverse('accounts:login'))
            else:
                try:
                    username = User.objects.get(username=name)
                except:                    
                    messages.error(request, 'Username is incorrect')
                    return HttpResponseRedirect(reverse('accounts:login'))
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}')
                return HttpResponseRedirect(reverse('website:index'))
            else:
                messages.error(request, 'Inputs are incorrect')
                return HttpResponseRedirect(reverse('accounts:login'))
        else:
            return render(request,'accounts/login.html')

    return HttpResponseRedirect(reverse('website:index'))



def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request,username=username, password=password)

            if (user is None) and (form.is_valid()):                
                user = form.save(commit=False)
                email = request.POST['email'] 
                try:
                    unique_mail = User.objects.get(email=email)
                except :
                    # we want unique email
                    user.email = email
                    if request.POST['first_name'] != None:
                        first_name = request.POST['first_name']
                        user.first_name = first_name
                    if request.POST['last_name'] != None:
                        last_name = request.POST['last_name']
                        user.last_name = last_name
                        
                    user.save()
                    user = authenticate(request,username=username, password=password) 
                    login(request,user)
                    messages.success(request,'User created successfully')
                    messages.success(request,f'Welcome {username}')
                    return HttpResponseRedirect(reverse('website:index'))
                else:
                    
                    messages.error(request, 'This Email is already taken')
                    messages.error(request, form.errors)                
                    return HttpResponseRedirect(reverse('accounts:signup'))
                
            else:
                messages.error(request, 'Inputs are incorrect')
                messages.error(request, form.errors)                
                return HttpResponseRedirect(reverse('accounts:signup'))
                
        elif request.method == "GET":
            form = UserCreationForm()
            context = {
                'form':form
            }
            return render(request,'accounts/signup.html',context)
    else:
        return HttpResponseRedirect(reverse('website:index'))
    
    
@login_required(redirect_field_name='/')
def logout_view(request):
 
    logout(request)
    messages.success(request, 'Successfully logged out')      
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
