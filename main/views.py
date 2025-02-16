from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from .utils import get_client_ip
from .models import CategoryModel, ItemModel, LinkModel, LinkClickModel, LinkActionModel


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
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "category-items.html",
            {"items": page_obj, "category": category, "page_obj": page_obj},
        )


class SearchView(View):
    def get(self, request):
        query = request.GET.get("q")
        items = ItemModel.objects.filter(title__icontains=query) if query else []
        paginator = Paginator(items, 10)  # Show 10 items per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "search.html", {"items": page_obj})


class ItemView(View):
    def get(self, request, item_slug):
        item = ItemModel.objects.get(slug=item_slug)
        working_links = (
            item.linkmodel_set.filter(status="working")
            .annotate(total_clicks=Count("linkclickmodel"))
            .exclude(id__in=[link.id for link in item.linkmodel_set.all() if link.spam_count() >= 50])
            .order_by("-total_clicks")
        )
        not_verified_links = (
            item.linkmodel_set.filter(status="not_verified")
            .annotate(total_clicks=Count("linkclickmodel"))
            .exclude(id__in=[link.id for link in item.linkmodel_set.all() if link.spam_count() >= 50])
            .order_by("-total_clicks")
        )
        not_working_links = (
            item.linkmodel_set.filter(status="not_working")
            .annotate(total_clicks=Count("linkclickmodel"))
            .exclude(id__in=[link.id for link in item.linkmodel_set.all() if link.spam_count() >= 50])
            .order_by("-total_clicks")
        )
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




class LinkView(View):
    def get(self, request, link_id):
        # Update link click count
        link = LinkModel.objects.get(id=link_id)
        link_click = LinkClickModel(link=link)
        link_click.save()

        # Redirect to the link
        return redirect(link.url)


class SubmitLinkView(View):
    def post(self, request):
        url = request.POST.get("url")
        item_id = request.POST.get("item_id")
        if not url or not item_id:
            return HttpResponseBadRequest("URL and Item ID are required")

        item = ItemModel.objects.get(id=item_id)
        LinkModel.objects.get_or_create(url=url, item=item)
        return redirect("item", item.slug)


class ReportLinkWorkingView(View):
    def post(self, request, link_id):
        ip_address = get_client_ip(request)
        link = get_object_or_404(LinkModel, id=link_id)
        LinkActionModel.objects.get_or_create(
            link=link, ip_address=ip_address, action="working"
        )
        return redirect(request.META.get("HTTP_REFERER", "home"))


class ReportLinkBrokenView(View):
    def post(self, request, link_id):
        ip_address = get_client_ip(request)
        link = get_object_or_404(LinkModel, id=link_id)
        LinkActionModel.objects.get_or_create(
            link=link, ip_address=ip_address, action="not_working"
        )
        return redirect(request.META.get("HTTP_REFERER", "home"))


class ReportLinkSpamView(View):
    def post(self, request, link_id):
        ip_address = get_client_ip(request)
        link = get_object_or_404(LinkModel, id=link_id)
        LinkActionModel.objects.get_or_create(
            link=link, ip_address=ip_address, action="spam"
        )
        return redirect(request.META.get("HTTP_REFERER", "home"))


class PrivacyPolicyView(View):
    def get(self, request):
        return render(request, "privacy-policy.html")