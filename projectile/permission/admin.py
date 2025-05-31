from django.contrib import admin

from .models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "description")
    search_fields = ("uid", "name", "description")
    list_filter = ("is_deleted",)
    list_per_page = 50
