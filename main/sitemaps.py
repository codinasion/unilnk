from django.contrib.sitemaps import Sitemap, GenericSitemap
from django.core.paginator import Paginator
from django.urls import reverse
from .models import ItemModel


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
    limit = 50000

    def items(self):
        return ItemModel.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()

    def get_sitemaps(self):
        paginator = Paginator(self.items(), self.limit)
        sitemaps = {}
        for page_number in paginator.page_range:
            sitemaps[f"items_page_{page_number}"] = GenericSitemap(
                {
                    "queryset": paginator.page(page_number).object_list,
                    "date_field": "created_at",
                },
                priority=self.priority,
                changefreq=self.changefreq,
            )
        return sitemaps
