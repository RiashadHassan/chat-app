from django.urls import path, include
urlpatterns = [
    path("users/", include("projectile.aquila.rest.urls.user")),
    path("health/", include("projectile.aquila.rest.urls.health")),

]