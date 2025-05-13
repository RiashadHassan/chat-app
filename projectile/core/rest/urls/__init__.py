from django.urls import path, include


urlpatterns = [
    path("users/", include("projectile.core.rest.urls.user"))
]