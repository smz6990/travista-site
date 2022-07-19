from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', blog_index,name='index'),
    path('<int:id>/',blog_single,name='single'),
    path('category/<str:cat_name>/',blog_index,name='category'),
    path('author/<str:author_username>/',blog_index,name='author'),
    path('search/',blog_search,name='search'),
    path('test/',test,name='single'),
    
]
