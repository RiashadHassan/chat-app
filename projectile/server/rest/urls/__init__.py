from django.urls import path, include


urlpatterns = [
    path("", include("server.rest.urls.server")),
    path(
        "<uuid:server_uid>/categories/",
        include("server.rest.urls.category"),
    ),
    path(
        "<uuid:server_uid>/invites/",
        include("server.rest.urls.invite"),
    ),
    path(
        "<uuid:server_uid>/roles/",
        include("server.rest.urls.role"),
    ),
]
