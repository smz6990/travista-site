from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', index_view,name='index'),
    path('single/',single_view,name='single'),
    
]
