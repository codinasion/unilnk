from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
from django.core.paginator import Paginator
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
        category = CategoryModel.objects.get(slug=category_slug)
        items = ItemModel.objects.filter(category__slug=category_slug)
        paginator = Paginator(items, 10)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "category-items.html", {"items": page_obj, "category": category, "page_obj": page_obj})


class SearchView(View):
    def get(self, request):
        query = request.GET.get("q")
        items = ItemModel.objects.filter(title__icontains=query) if query else []
        paginator = Paginator(items, 10)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "search.html", {"items": page_obj})


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


class LinkView(View):
    def get(self, request, link_id):
        # Update link click count
        link = LinkModel.objects.get(id=link_id)
        link_click = LinkClickModel(link=link)
        link_click.save()

        # Redirect to the link
        return redirect(link.url)
