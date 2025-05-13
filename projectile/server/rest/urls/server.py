from django.urls import path
from ..views.server import (
    ServerListCreateView,
    ServerRetrieveView,
    ServerUpdateView,
    ServerDestroyView,
)

urlpatterns = [
    path("", ServerListCreateView.as_view(), name="server-list-create"),
    path(
        "<uuid:uid>/", ServerRetrieveView.as_view(), name="server-list-create"
    ),
    path("<uuid:uid>/update/", ServerUpdateView.as_view(), name="server-details"),
    path("<uuid:uid>/delete/", ServerDestroyView.as_view(), name="server-update"),
]
