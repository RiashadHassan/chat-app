from django.urls import path, include

from connection.rest.views.request import ConnectionRequestListView, ConnectionRequestCreateView

urlpatterns = [
    path("", ConnectionRequestListView.as_view(), name="connection-requests-list"),
    path("send/", ConnectionRequestCreateView.as_view(), name="connection-requests-create")
]
