from django.urls import path
from .views import *
from blog.feeds import LatestEntriesFeed

app_name = 'blog'

urlpatterns = [
    path('', blog_index,name='index'),
    path('<int:id>/',blog_single,name='single'),
    path('comment-<int:id>/',blog_comment,name='comment'),
    path('category/<str:cat_name>/',blog_index,name='category'),
    path('tag/<str:tag_name>/',blog_index,name='tag'),
    path('author/<str:author_username>/',blog_index,name='author'),
    path('search/',blog_search,name='search'),
    path('rss/feed/', LatestEntriesFeed()),
    
]
