from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import Post,Category

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    
    date_hierarchy = 'created_date'
    empty_value_display = '-empty-'
    # fields = ('author','title','content','status','published_date',)
    list_display = ('title' ,'author','counted_views','status','published_date','created_date')
    list_filter = ('status','author',)
    search_fields = ['title','content']
    summernote_fields = ('content',)
    
admin.site.register(Category)