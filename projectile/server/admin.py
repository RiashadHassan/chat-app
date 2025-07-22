from django.contrib import admin

from server.models import (
    Server,
    Category,
    Channel,
    Thread,
    Role,
    RolePermission,
)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("uid", "slug", "owner", "icon_url", "banner_url")
    list_filter = ("member_limit", "is_deleted")

    search_fields = (
        "uid",
        "slug",
        "owner_uid",
        "description",
        "icon_url",
        "banner_url",
    )
    list_per_page = 50
    raw_id_fields = ("owner",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("owner")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("uid", "slug", "server")
    search_fields = ("uid", "slug", "name", "server_uid")
    list_per_page = 50
    raw_id_fields = ("server",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("server")


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "slug", "server", "category")
    list_filter = ("is_private",)

    search_fields = ("uid", "name", "slug", "server_uid", "category_uid")
    list_per_page = 50
    raw_id_fields = ("server", "category")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("server", "category")


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "slug", "server", "category", "channel")
    list_filter = ("is_archived", "auto_archive_duration")

    search_fields = ("uid", "name", "slug", "server_uid", "category_uid", "channel_uid")
    list_per_page = 50
    raw_id_fields = ("server", "category", "channel")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("server", "category", "channel")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "server", "position")
    search_fields = (
        "uid",
        "name",
        "slug",
        "server_uid",
        "server__name",
    )
    list_per_page = 50
    raw_id_fields = ("server",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("server", "server__owner")


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "permission")
    search_fields = ("role__name", "role_uid", "permission_uid", "permission__name")
    list_per_page = 50
    raw_id_fields = ("role", "permission")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("role", "permission")
