from django.urls import path

from connection.rest.views.connection import (
    UserConnectionListView,
    UserConnectionDetailsView,
)

urlpatterns = [
    path("", UserConnectionListView.as_view(), name="user-connection-list"),
    path(
        "<uuid:uid>",
        UserConnectionDetailsView.as_view(),
        name="user-connection-details",
    ),
]
