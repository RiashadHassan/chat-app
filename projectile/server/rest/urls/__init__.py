from django.urls import path, include


urlpatterns = [
    path("", include("projectile.server.rest.urls.server")),
    path(
        "<uuid:server_uid>/categories/",
        include("projectile.server.rest.urls.category"),
    ),
    path(
        "<uuid:server_uid>/invites/",
        include("projectile.server.rest.urls.invite"),
    ),
    path(
        "<uuid:server_uid>/roles/",
        include("projectile.server.rest.urls.role"),
    ),
]
