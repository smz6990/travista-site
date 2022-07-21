from django.contrib.syndication.views import Feed
from blog.models import Post

class LatestEntriesFeed(Feed):
    title = "Latest posts"
    link = "/rss/feed/"
    description = "All posts from our site"

    def items(self):
        return Post.objects.filter(status=True)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:50]
