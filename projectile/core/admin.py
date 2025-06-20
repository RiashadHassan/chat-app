from django.contrib import admin
from django.contrib.auth import get_user_model

from projectile.core.models import Spectrum

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "uid", "first_name", "last_name")
    list_filter = ("status", "is_verified", "is_staff")

    search_fields = ("username", "email", "phone", "uid", "first_name", "last_name")
    list_per_page = 50

@admin.register(Spectrum)
class SpectrumAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_filter = ("is_deleted",)

    search_fields = ("name", "slug")
    list_per_page = 50

