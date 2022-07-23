from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from accounts.forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm



def login_view(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST': 
            password = request.POST['password']    
            
            if request.POST['username'] != None and request.POST['username'] != '':
                username = request.POST['username']
                user = authenticate(request, username=username, password=password)
                
            # elif request.POST['email'] != None:
            #     email = request.POST['email']
            #     username = User.objects.get(email=email)
            #     user = authenticate(request, username=username, email=email, password=password)
                
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
            email = request.POST['email']
            password = request.POST['password1']
            user = authenticate(request,username=username, password=password)
            if (user is None) and (form.is_valid()):
                user = form.save(commit=False)
                user.email = email
                user.save()
                user = authenticate(request,username=username, password=password) 
                login(request,user)
                messages.success(request,'User created successfully')
                messages.success(request,f'Welcome {username}')
                return HttpResponseRedirect(reverse('website:index'))
            
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
        
        
        
    #     if request.method =='POST':
    #         form = SignUpForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             username = request.POST['username']
    #             email = request.POST['email']
    #             password = request.POST['password']
    #             user = authenticate(request, username=username, email=email, password=password)
    #             login(request,user)
    #             messages.success(request, f'Welcome {username}')
    #             return HttpResponseRedirect(reverse('website:index'))
    #         else:
    #             messages.error(request,'Inputs are incorrect')
    #             messages.error(request,form.errors)
    #             return HttpResponseRedirect(reverse('accounts:signup',kwargs={'form':form}))
    #     else: # GET
    #         form = SignUpForm()
    #         return render(request,'accounts/signup.html',{'form':form})
    # else: # is_authenticated
    #     return HttpResponseRedirect(reverse('website:index'))
   
    


@login_required(redirect_field_name='/')
def logout_view(request):
 
    logout(request)
    messages.success(request, 'Successfully logged out')      
    return HttpResponseRedirect(reverse('website:index'))