from django.urls import path, include


urlpatterns = [
    path("", include("member.rest.urls.member")),
]
