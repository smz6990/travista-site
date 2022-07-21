from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(status=True)

    def lastmod(self, obj):
        return obj.published_date
    
    def location(self,item):
        return reverse('blog:single',kwargs={'id':item.id})