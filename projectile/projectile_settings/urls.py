from django.urls import path, include
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


project_urls = [
    # for system administration only
    path("api/aquila/", include("projectile.aquila.rest.urls")),
    # for users (DB CRUD)
    path("api/v1/core/", include("projectile.core.rest.urls")),
    path("api/v1/servers/", include("projectile.server.rest.urls")),
    path(
        "api/v1/servers/<uuid:server_uid>/members/",
        include("projectile.member.rest.urls"),
    ),
    # for cache and search
    path("api/v1/search/", include("projectile.elastic.rest.urls")),
]

ws_urls = [
    path("ws/v1/chat/", include("projectile.chat.urls")),
]


django_app_urls = [
    path("admin/", admin.site.urls),
    path("auth/", include("rest_framework.urls")),
]

package_urls = [
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Profilers
    path("silk/", include("silk.urls", namespace="silk")),
]


urlpatterns = project_urls + ws_urls + django_app_urls + package_urls
