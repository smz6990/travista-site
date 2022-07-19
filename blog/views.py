from django.shortcuts import render,get_object_or_404
from django.http import Http404
from blog.models import Post

# from django.core.paginator import Paginator

from django.utils import timezone
# Create your views here.

def index_view(request):
    
    now = timezone.now()
    posts = Post.objects.filter(published_date__lte=now)
    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)


def single_view(request,id):
    
    now = timezone.now()
    posts = Post.objects.filter(published_date__lte=now)
    post = get_object_or_404(posts,id=id)
    if post:
        post.counted_views += 1
        post.save()
        nextpost = Post.objects.filter(published_date__gt=post.published_date).exclude(published_date__gt=now).order_by('published_date').first()
        prevpost = Post.objects.filter(published_date__lt=post.published_date).exclude(published_date__gt=now).order_by('published_date').last()
        context = { 'post':post , 'nextpost':nextpost , 'prevpost':prevpost }
        return render(request,'blog/blog-single.html',context)
    
    # raise 404 page not found if the post is not published yet
    raise Http404("There is no post with the given id")
    
def test(request):
    return render(request,'test.html')