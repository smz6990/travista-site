from django import template
from blog.models import Post

from django.utils import timezone

register = template.Library()

@register.simple_tag(name='postCount')
def function():
    posts_count = Post.objects.filter(published_date__lte=timezone.now()).count()
    return posts_count

@register.simple_tag(name='posts')
def function():
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return posts

@register.filter(name='snippet')
def function(value,arg=20):    
    return value[:arg] + ('...' if len(value)> arg else '' )

@register.inclusion_tag('blog/blog-popular-post.html')
def popular_posts(arg=4):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-counted_views')[:arg]
    return {'posts':posts}    