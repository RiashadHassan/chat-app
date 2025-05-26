from django.urls import path
from ..views.user import (
    UserListView,
    UserRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", UserListView.as_view(), name="list-user"),
    path(
        "<uuid:uid>/",
        UserRetrieveUpdateDestroyView.as_view(),
        name=("retrieve-update-destroy-user"),
    ),
]
