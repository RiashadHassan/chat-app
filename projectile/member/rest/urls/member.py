from django.urls import path
from ..views.member import (
    ServerJoinView,
    ServerLeaveView,
    MemberListView,
    MemberDetailsView,
)

urlpatterns = [
    path("join/", ServerJoinView.as_view(), name="member-join-server"),
    path("leave/", ServerLeaveView.as_view(), name="member-leave-server"),
    path("<uuid:member_uid>/", MemberDetailsView.as_view(), name="member-details"),
    path("", MemberListView.as_view(), name="member-list"),
]
