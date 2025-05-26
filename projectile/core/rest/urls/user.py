from django.urls import path
from ..views.user import (
    UserRegisterView,
    PrivateUserDetailsView,
    PrivateUserDestroyView,
)

urlpatterns = [
    # public
    path("register/", UserRegisterView.as_view(), name="register-user"),
    # for user
    path("me/", PrivateUserDetailsView.as_view(), name=("user-profile")),
    path("me/delete/", PrivateUserDestroyView.as_view(), name=("user-profile")),
]
