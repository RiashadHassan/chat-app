from django.urls import path
from ..views.user import (
    UserListView,
    UserDetailsView,
)

urlpatterns = [
    path("", UserListView.as_view(), name="list-user"),
    path(
        "<uuid:uid>/",
        UserDetailsView.as_view(),
        name=("retrieve-update-destroy-user"),
    ),
]
