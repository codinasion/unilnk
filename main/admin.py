from django.contrib import admin
from .models import CategoryModel, ItemModel, LinkModel, LinkClickModel


@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    search_fields = ("title",)
    fields = ("title",)


@admin.register(ItemModel)
class ItemModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "category",
        "get_total_clicks",
    )
    search_fields = ("title",)
    list_filter = ("category",)
    fields = ("title", "category")

    def get_total_clicks(self, obj):
        return obj.get_total_clicks()

    get_total_clicks.short_description = "Clicks"


@admin.register(LinkModel)
class LinkModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "item",
        "url",
        "status",
        "get_working_count",
        "get_not_working_count",
        "get_total_clicks",
    )
    search_fields = ("url",)
    list_filter = ("status",)
    fields = ("item", "url", "status")

    def get_working_count(self, obj):
        return obj.working_count

    get_working_count.short_description = "Working"

    def get_not_working_count(self, obj):
        return obj.not_working_count

    get_not_working_count.short_description = "Not Working"

    def get_total_clicks(self, obj):
        return obj.get_total_clicks()

    get_total_clicks.short_description = "Clicks"


@admin.register(LinkClickModel)
class LinkClickModelAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "created_at")
    search_fields = ("link",)
    list_filter = ("created_at",)
    fields = ("link",)
