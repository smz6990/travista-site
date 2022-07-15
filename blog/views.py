from django.shortcuts import render
from blog.models import Post
# Create your views here.

def index_view(request):
    posts = Post.objects.filter(status=1)
    context = {'posts':posts}
    return render(request,'blog/blog-home.html',context)

def single_view(request):
    return render(request,'blog/blog-single.html')