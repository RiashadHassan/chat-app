from django.db.models import QuerySet

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from server.models import Server

from ...models import Member
from ..serializers.member import (
    MemberListCreateSerializer,
    MemberDetailsSerializer,
)


class ServerJoinView(CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self) -> dict:
        server = get_object_or_404(Server, uid=self.kwargs.get("server_uid"))
        context = super().get_serializer_context()
        context["request"] = self.request
        context["server"] = server
        return context


class ServerLeaveView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Member:
        try:
            return Member.objects.get(
                user_uid=self.request.user.uid,
                server_uid=self.kwargs.get("server_uid"),
                is_deleted=False,
            )
        except Member.DoesNotExist:
            raise exceptions.NotFound(detail="You are not a member of this server.")

    def perform_destroy(self, instance: Member) -> None:
        instance.is_deleted = True
        instance.save()


class MemberListView(ListAPIView):
    serializer_class = MemberListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Member]:
        return Member.objects.filter(
            server_uid=self.kwargs.get("server_uid"), is_deleted=False
        ).select_related("user", "server")


class MemberDetailsView(RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Member:
        member = get_object_or_404(Member, uid=self.kwargs.get("member_uid"))
        if member.server_uid != str(self.kwargs.get("server_uid")):
            raise exceptions.NotFound(detail="Server not found.")
        return member
