from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



def login_view(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST': 
            password = request.POST['password']    
            
            name = request.POST['username']
            if '@' in name:
                username = User.objects.get(email=name)
            else:
                username = name
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