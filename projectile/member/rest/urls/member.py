from django.urls import path
from ..views.member import (
    MemberCreateView,
    MemberListView,
    MemberDetailsView,
    MemberDestroyView,
)

urlpatterns = [
    path("", MemberListView.as_view(), name="member-list"),
    path("", MemberCreateView.as_view(), name="member-create"),
    path(
        "<uuid:m_uid>/",
        MemberDetailsView.as_view(),
        name="member-retreive-update",
    ),
    path("<uuid:m_uid>/destroy/", MemberDestroyView.as_view(), name="member-destroy"),
]
