from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import  messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import NewUserFrom

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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
                    return redirect(reverse('accounts:login'))
            else:
                username = request.POST['username']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f'Welcome back {username}')
                if 'next' in request.POST:
                    return redirect (request.POST.get('next','/'))
                return redirect('/')
            else:
                messages.error(request,'Invalid username\email or password')
        
        return render(request,'accounts/login.html')
    return redirect('/')


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = NewUserFrom(request.POST)
            email = request.POST['email']
            try:
                User.objects.get(email=email)
            except :
                pass
            else:
                messages.error(request,'This email is taken')
                form = NewUserFrom()
                context = {
                    'form':form
                    }
                return render(request,'accounts/signup.html',context)
            if form.is_valid():
                user = form.save()
                login(request,user)
                messages.success(request,'Account created successfully')
                messages.success(request,f'Welcome {user.username}')
                if 'next' in request.POST:
                    return redirect (request.POST.get('next','/'))
                return redirect(reverse('website:index'))
            messages.error(request,'Invalid information')
            messages.error(request,form.errors)
        form = NewUserFrom()
        context = {
            'form':form
            }
        return render(request,'accounts/signup.html',context)
    return redirect(reverse('website:index'))
    
    
    
@login_required()
def logout_view(request):
 
    logout(request)
    messages.info(request, 'Successfully logged out') 
    if 'next' in request.GET:
        return redirect (request.GET.get('next','/'))     
    return redirect(reverse('website:index'))


def password_reset_request_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('website:index'))
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect ("/accounts/password_reset/done/")
                   # return redirect(reverse("accounts:password_reset_done")) #
                messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})
