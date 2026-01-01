from django.urls import path, include

from connection.rest.views.request import (
    ConnectionRequestCreateView,
    SentConnectionRequestListView,
    ReceivedConnectionRequestListView,
    SentConnectionRequestDetailsView,
    ReceivedConnectionRequestDetailsView,
    RejectConnectionRequestView,
    CancelConnectionRequestView,
    AcceptConnectionRequestView,
)

urlpatterns = [
    path(
        "send/",
        ConnectionRequestCreateView.as_view(),
        name="connection-requests-create",
    ),
    path(
        "sent/",
        SentConnectionRequestListView.as_view(),
        name="sent-connection-requests-list",
    ),
    path(
        "sent/<uuid:request_uid>/",
        SentConnectionRequestDetailsView.as_view(),
        name="sent-connection-requests-detail",
    ),
    path(
        "sent/<uuid:request_uid>/cancel/",
        CancelConnectionRequestView.as_view(),
        name="cancel-connection-requests",
    ),
    path(
        "received/",
        ReceivedConnectionRequestListView.as_view(),
        name="received-connection-requests-list",
    ),
    path(
        "received/<uuid:request_uid>/",
        ReceivedConnectionRequestDetailsView.as_view(),
        name="received-connection-requests-detail",
    ),
    path(
        "received/<uuid:request_uid>/reject/",
        RejectConnectionRequestView.as_view(),
        name="reject-connection-requests",
    ),
    path(
        "received/<uuid:request_uid>/accept/",
        AcceptConnectionRequestView.as_view(),
        name="accept-connection-requests",
    ),
]
