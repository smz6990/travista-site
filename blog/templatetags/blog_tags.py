from django import template
from blog.models import Post,Category,Comment

from django.utils import timezone

register = template.Library()

@register.simple_tag(name='comments_count')
def function(id):
    return Comment.objects.filter(post=id,approved=True).count()
    


@register.inclusion_tag('blog/blog-popular-post.html')
def popular_posts(arg=4):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-counted_views')[:arg]
    return {'posts':posts}

@register.inclusion_tag('blog/blog-post-categories.html')
def post_categories():
    posts = Post.objects.filter(published_date__lte=timezone.now())
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()
    return {'categories':cat_dict}