from django.contrib import admin
from blog.models import Post,Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    # fields = ('author','title','content','status','published_date',)
    list_display = ('title' ,'author','counted_views','status','published_date','created_date')
    list_filter = ('status','author',)
    search_fields = ['title','content']
    
admin.site.register(Category)