from django.urls import path

from ..views.invite import InviteListCreateView, AcceptInviteView

urlpatterns = [
    path("", InviteListCreateView.as_view(), name="invite-list-create"),
    path("<str:code>/accept/", AcceptInviteView.as_view(), name="accept-invite"),
]
