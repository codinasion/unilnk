from django.contrib import admin
from . import models


@admin.register(models.ServerUpdateModel)
class ServerUpdateAdmin(admin.ModelAdmin):
    list_display = ("server_update_time", "server_update_status")
    list_filter = ("server_update_time", "server_update_status")
    search_fields = ("server_update_time", "server_update_status")
    ordering = ("-server_update_time",)
    fields = ("server_update_time", "server_update_status", "server_update_error")
    readonly_fields = ("server_update_time", "server_update_status", "server_update_error")
