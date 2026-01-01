from django.contrib import admin

from connection.models import ConnectionRequest, ConnectionBlock, UserConnection


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("uid", "sender", "receiver", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("uid", "sender_uid", "receiver_uid")
    list_per_page = 50
    raw_id_fields = ("sender", "receiver")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("sender", "receiver")


@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    list_display = ("uid", "left_user", "right_user", "created_at")
    search_fields = ("uid", "left_user_uid", "right_user_uid")
    list_per_page = 50
    raw_id_fields = ("left_user", "right_user")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("left_user", "right_user")


@admin.register(ConnectionBlock)
class ConnectionBlockAdmin(admin.ModelAdmin):
    list_display = ("uid", "blocker", "blocked", "created_at")
    search_fields = ("uid", "blocker_uid", "blocked_uid")
    list_per_page = 50
    raw_id_fields = ("blocker", "blocked")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("blocker", "blocked")
