from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("ws/v1/chat/", include("projectile.chat.urls")),
    path("api/v1/core/", include("projectile.core.rest.urls")),

]
