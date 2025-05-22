from django.urls import path, include


urlpatterns = [
    path("", include("projectile.member.rest.urls.member")),
]
