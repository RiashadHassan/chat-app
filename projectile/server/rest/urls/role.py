from django.urls import path

from ..views.role import RoleListCreateView, RoleDetailsView

urlpatterns = [
    path("", RoleListCreateView.as_view(), name="role-list-create"),
    path("<uuid:role_uid>", RoleDetailsView.as_view(), name="role-details"),
]
