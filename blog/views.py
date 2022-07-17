from django.shortcuts import render,get_object_or_404
from django.http import Http404
from blog.models import Post

from django.utils import timezone
# Create your views here.

def index_view(request):
    # posts = Post.objects.filter(status=1)
    now = timezone.now()
    posts = Post.objects.filter(published_date__lte=now)
            
    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)


def single_view(request,pid):
    post = get_object_or_404(Post,id=pid)
    now = timezone.now()
    
    if now > post.published_date:
        post.counted_views += 1
        post.save()
        context = {'post':post}
        return render(request,'blog/blog-single.html',context)
    
    # raise 404 page not found if the post is not published yet
    raise Http404("There is no post with the given id")
    