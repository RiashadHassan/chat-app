from django.contrib import admin

from .models import *


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("uid", "user", "user_uid", "server", "server_uid")
    list_filter = ("is_deleted",)
    search_fields = ("uid", "user", "user_uid", "server", "server_uid")
    list_per_page = 50

    raw_id_fields = ("user", "server")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user", "server")
