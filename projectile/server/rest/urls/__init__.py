from django.urls import path, include


urlpatterns = [
    path("", include("projectile.server.rest.urls.server"))
]