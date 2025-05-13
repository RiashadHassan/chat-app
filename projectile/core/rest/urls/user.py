from django.urls import path
from ..views.user import (
    UserListView,
    UserRegisterView,
    UserRetrieveUpdateView,
    UserDestroyView,
    PrivateUserDetailsView,
    PrivateUserDestroyView,
)

urlpatterns = [
    # public
    path("register/", UserRegisterView.as_view(), name="register-user"),
    # for user
    path("me/", PrivateUserDetailsView.as_view(), name=("user-profile")),
    path("me/delete/", PrivateUserDestroyView.as_view(), name=("user-profile")),
    # for system admins
    path("list/", UserListView.as_view(), name="list-user"),
    path(
        "<uuid:uid>/update/",
        UserRetrieveUpdateView.as_view(),
        name=("retrieve-update-user"),
    ),
    path("<uuid:uid>/delete/", UserDestroyView.as_view(), name=("destroy-user")),
]
