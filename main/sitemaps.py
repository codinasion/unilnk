from django.contrib.sitemaps import Sitemap
from .models import ItemModel
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ["home", "categories", "search", "privacy_policy"]

    def location(self, item):
        return reverse(item)


class ItemSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ItemModel.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()
