from django.contrib import admin
from .models import CategoryModel, ItemModel, LinkModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ItemModel)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "category")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(LinkModel)
class LinkModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "item",
        "url",
        "status",
        "working_count",
        "not_working_count",
        "click_count",
    )
    search_fields = ("url",)
    list_filter = ("status",)
