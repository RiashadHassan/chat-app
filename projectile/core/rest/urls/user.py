from django.urls import path
from ..views.user import (
    UserRegisterView,
    PrivateUserDetailsView,
    PrivateUserDestroyView,
    LoginView,
)

urlpatterns = [
    # public
    path("register/", UserRegisterView.as_view(), name="register-user"),
    path("login/", LoginView.as_view(), name="login-user"),
    # for user
    path("me/", PrivateUserDetailsView.as_view(), name=("user-profile")),
    path("me/delete/", PrivateUserDestroyView.as_view(), name=("user-profile")),
]
