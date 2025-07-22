from django.urls import path, include
urlpatterns = [
    path("users/", include("aquila.rest.urls.user")),
    path("health/", include("aquila.rest.urls.health")),

]