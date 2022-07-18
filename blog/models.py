from django.db import models
from django.contrib.auth.models import User

class Post (models.Model):
    
    # image = models.ImageField()
    
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    # tags 
    # category
    counted_views = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_date']
    
    def __str__(self):
        return ' {} - {} '.format(self.id,self.title)
