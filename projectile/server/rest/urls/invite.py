from django.urls import path

from ..views.invite import InviteListCreateView, AcceptInviteView, ExpireInviteView

urlpatterns = [
    path("", InviteListCreateView.as_view(), name="invite-list-create"),
    path("<str:code>/expire/", ExpireInviteView.as_view(), name="expire-invite"),
    path("<str:code>/accept/", AcceptInviteView.as_view(), name="accept-invite"),
]
