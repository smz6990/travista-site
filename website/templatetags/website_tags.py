from django import template
from blog.models import Post

from django.utils import timezone

register = template.Library()

@register.inclusion_tag('website/recent-blog-post.html')
def latestposts(arg=6):
    posts = Post.objects.filter(published_date__lte=timezone.now())[:arg]
    return {'posts':posts}