from django.urls import path, include


urlpatterns = [
    path("user/", include("projectile.core.rest.urls.user"))
]