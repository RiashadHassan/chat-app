from django.urls import path, include


urlpatterns = [
    path("users/", include("core.rest.urls.user"))
]