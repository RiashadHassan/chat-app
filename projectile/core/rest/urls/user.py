from django.urls import path
from ..views.user import UserRegisterView, UserRetrieveUpdateView, UserDestroyView, PrivateUserManageView, PrivateUserDestroyView

urlpatterns = [
    # public
    path("register/", UserRegisterView.as_view(), name="register-user"),
    # for users
    path("me/", PrivateUserManageView.as_view(), name=("user-profile")),
    path("me/delete/", PrivateUserDestroyView.as_view(), name=("user-profile")),
    # for system admins
    path(
        "update/<uuid:uid>/",
        UserRetrieveUpdateView.as_view(),
        name=("retrieve-update-user"),
    ),
    path("delete/<uuid:uid>/", UserDestroyView.as_view(), name=("destroy-user")),
]
