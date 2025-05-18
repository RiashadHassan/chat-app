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


django_app_urls = [
    path("admin/", admin.site.urls),
    path("auth/", include("rest_framework.urls")),
    path("ws/v1/chat/", include("projectile.chat.urls")),
    path("api/v1/core/", include("projectile.core.rest.urls")),
    path("api/v1/servers/", include("projectile.server.rest.urls")),
    path("api/v1/search/", include("projectile.elastic.rest.urls")),

]

jwt_urls = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]


swagger_urls = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

profiler_urls = [path("silk/", include("silk.urls", namespace="silk"))]


urlpatterns = django_app_urls + jwt_urls + swagger_urls + profiler_urls
