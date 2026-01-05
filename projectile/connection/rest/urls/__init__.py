from django.urls import path, include


urlpatterns = [
    path("requests/", include("connection.rest.urls.request")),
    # path("blocks", include("connection.rest.urls.block")),
    path("connections/", include("connection.rest.urls.connection")),
]
