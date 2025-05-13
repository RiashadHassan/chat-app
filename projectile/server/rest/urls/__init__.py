from django.urls import path, include


urlpatterns = [
    path("servers/", include("projectile.server.rest.urls.server"))
]