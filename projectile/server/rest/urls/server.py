from django.urls import path
from ..views.server import (
    ServerListCreateView,
    ServerDetailsView,
    )

urlpatterns = [
    path("", ServerListCreateView.as_view(), name="server-list-create"),
    path(
        "<uuid:uid>/", ServerDetailsView.as_view(), name="server-details"
    ),
]
