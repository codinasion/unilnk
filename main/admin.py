from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import CategoryModel, ItemModel, LinkModel, LinkClickModel, LinkActionModel


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fields = ("session_key", "session_data", "expire_date")
    readonly_fields = ("session_key", "session_data", "expire_date")


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
        "get_spam_count",
        "get_total_clicks",
    )
    search_fields = ("url",)
    list_filter = ("status",)
    fields = ("item", "url", "status")

    def get_working_count(self, obj):
        return obj.working_count()

    get_working_count.short_description = "Working"

    def get_not_working_count(self, obj):
        return obj.not_working_count()

    get_not_working_count.short_description = "Not Working"

    def get_spam_count(self, obj):
        return obj.spam_count()

    get_spam_count.short_description = "Spam"

    def get_total_clicks(self, obj):
        return obj.get_total_clicks()

    get_total_clicks.short_description = "Clicks"


@admin.register(LinkActionModel)
class LinkActionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "action", "created_at")
    search_fields = ("link", "action")
    list_filter = ("action", "created_at")
    fields = ("link", "action", "created_at")
    readonly_fields = ("link", "action", "created_at")


@admin.register(LinkClickModel)
class LinkClickModelAdmin(admin.ModelAdmin):
    list_display = ("id", "link", "created_at")
    search_fields = ("link",)
    list_filter = ("created_at",)
    fields = ("link", "created_at")
    readonly_fields = ("link", "created_at")
