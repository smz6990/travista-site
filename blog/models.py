from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Category(models.Model):
    
    name =models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Post (models.Model):
    
    image = models.ImageField(upload_to = 'blog/' , default = 'blog/default.jpg')
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = TaggableManager() 
    category = models.ManyToManyField(Category)  
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)  
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return ' {} - {} '.format(self.id,self.title)
    
    def get_absolute_url(self):
        return reverse('blog:single',kwargs={'id':self.id})


class Comment(models.Model):
    
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_date']
        
    def __str__(self):
        return self.name