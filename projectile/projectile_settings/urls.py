from django.urls import path, include
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


django_app_urls = [
    path("admin/", admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path("ws/v1/chat/", include("projectile.chat.urls")),
    path("api/v1/core/", include("projectile.core.rest.urls")),
    path("api/v1/server/", include("projectile.server.rest.urls")),
]

jwt_urls = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


urlpatterns = django_app_urls + jwt_urls
