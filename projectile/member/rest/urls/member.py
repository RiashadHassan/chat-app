from django.urls import path
from ..views.member import (
    MemberListCreateView,
    MemberDetailsView,
    MemberDestroyView,
)

urlpatterns = [
    path("", MemberListCreateView.as_view(), name="member-list-create"),
    path(
        "<uuid:member_uid>/",
        MemberDetailsView.as_view(),
        name="member-retreive-update",
    ),
    path("<uuid:member_uid>/destroy/", MemberDestroyView.as_view(), name="member-destroy"),
]
