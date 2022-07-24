from django.urls import path ,reverse
from django.contrib.auth import views as auth_views

from accounts.views import *

app_name = 'accounts'
urlpatterns = [
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    
    path("password_reset/",
         password_reset_request_view ,
         name="password_reset"),
    
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html",post_reset_login=False,success_url='/accounts/reset/done/'),
         name='password_reset_confirm'),
    
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'), 
    
    
    
]