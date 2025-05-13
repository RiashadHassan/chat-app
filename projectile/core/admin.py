from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "uid", "first_name", "last_name")
    list_filter = ("status", "is_verified", "is_staff")

    search_fields = ("username", "email", "phone", "uid", "first_name", "last_name")
    list_per_page = 50
