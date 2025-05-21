from django.contrib import admin

from projectile.server.models import Server, Category, Channel, Thread #AuditLog


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("uid", "slug", "owner", "icon_url", "banner_url")
    list_filter = ("member_limit", "is_deleted")

    search_fields = ("uid", "slug", "owner", "description", "icon_url", "banner_url")
    list_per_page = 50


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("uid", "slug", "server")
    search_fields = ("uid", "slug", "server")
    list_per_page = 50


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "slug", "server", "category")
    list_filter = ("is_private",)

    search_fields = ("uid", "name", "slug", "server", "category")
    list_per_page = 50


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "slug", "server", "category", "channel")
    list_filter = ("is_archived", "auto_archive_duration")

    search_fields = ("uid", "name", "slug", "server", "category", "channel")
    list_per_page = 50


# @admin.register(AuditLog)
# class AuditLogAdmin(admin.ModelAdmin):
#     list_display = ("uid", "member", "server", "details")
#     list_filter = ("action",)

#     search_fields = ("uid", "member", "server", "details")
#     list_per_page = 50
