from django.shortcuts import render,get_object_or_404
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from blog.models import Post,Comment
from blog.forms import CommentForm
from django.contrib import  messages


from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.utils import timezone
# Create your views here.

def blog_index(request,**kwargs):
    
    now = timezone.now()
    posts = Post.objects.filter(published_date__lte=now)
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    
    if kwargs.get('author_username') != None :
        posts = posts.filter(author__username=kwargs['author_username'])
    
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])
        
    
    paginator = Paginator(posts,5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)



def blog_single(request,id):
    
    now = timezone.now()
    posts = Post.objects.filter(published_date__lte=now)
    post = get_object_or_404(posts,id=id)
    comments = Comment.objects.filter(post=post.id,approved=True)
    form = CommentForm()
    if post:
        post.counted_views += 1
        post.save()
        nextpost = Post.objects.filter(published_date__gt=post.published_date).exclude(published_date__gt=now). order_by('published_date').first()
        
        prevpost = Post.objects.filter(published_date__lt=post.published_date).exclude(published_date__gt=now).order_by('published_date').last()
        
        context = { 'post':post ,'form':form,'comments':comments, 'nextpost':nextpost , 'prevpost':prevpost }
        return render(request,'blog/blog-single.html',context)
    
    # raise 404 page not found if the post is not published yet
    raise Http404("There is no post with the given id")


def blog_comment(request,id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment submitted successfully.')
        else:
            messages.error(request, 'Invalid comment submission.')
            messages.error(request, form.errors)
            
    # reverse('edit_project', kwargs={'project_id':4})
    return HttpResponseRedirect(reverse('blog:single',kwargs={'id':id}))
    
    
def blog_search(request):
    now = timezone.now()
    posts = Post.objects.filter(published_date__lte=now)
    
    if request.method == "GET":
        if s := request.GET.get('s'):
            posts = posts.filter(content__contains = s)
    
    paginator = Paginator(posts,5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    
    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)