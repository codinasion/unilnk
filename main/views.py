from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.views import View
from django.db.models import Count
from .models import CategoryModel, ItemModel, LinkModel, LinkClickModel


class HomeView(View):
    def get(self, request):
        # trending items, most link clicked items in 24 hours
        trending_items = (
            ItemModel.objects.filter(
                linkmodel__linkclickmodel__created_at__gte=timezone.now()
                - timedelta(days=1)
            )
            .annotate(total_clicks=Count("linkmodel__linkclickmodel"))
            .order_by("-total_clicks")[:5]
        )
        print(trending_items)

        # most popular items, most link clicked items
        popular_items = ItemModel.objects.annotate(
            total_clicks=Count("linkmodel__linkclickmodel")
        ).order_by("-total_clicks")[:5]
        print(popular_items)

        # recently added items
        recent_items = ItemModel.objects.order_by("-created_at")[:5]
        print(recent_items)

        return render(
            request,
            "home.html",
            {
                "trending_items": trending_items,
                "popular_items": popular_items,
                "recent_items": recent_items,
            },
        )


class CategoriesView(View):
    def get(self, request):
        categories = CategoryModel.objects.all()
        return render(request, "categories.html", {"categories": categories})


class CategoryItemsView(View):
    def get(self, request, category_slug):
        items = ItemModel.objects.filter(category__slug=category_slug)
        return render(request, "category-items.html", {"items": items})


class SearchView(View):
    def get(self, request):
        return render(request, "search.html")


class ItemView(View):
    def get(self, request, item_slug):
        item = ItemModel.objects.get(slug=item_slug)
        working_links = item.linkmodel_set.filter(status="working")
        not_verified_links = item.linkmodel_set.filter(status="not_verified")
        not_working_links = item.linkmodel_set.filter(status="not_working")
        return render(
            request,
            "item.html",
            {
                "item": item,
                "working_links": working_links,
                "not_verified_links": not_verified_links,
                "not_working_links": not_working_links,
            },
        )


class NewItemView(View):
    def get(self, request):
        return render(request, "new-item.html")
