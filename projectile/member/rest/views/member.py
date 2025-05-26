from django.db.models import QuerySet

from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from projectile.server.models import Server

from ...models import Member
from ..serializers.member import (
    MemberListCreateSerializer,
    MemberDetailsSerializer,
)


class MemberListCreateView(ListCreateAPIView):
    """The create endpoint is basically the "join-server" functionality"""

    queryset = Member.objects.all()
    serializer_class = MemberListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[Member]:
        return Member.objects.filter(
            server_uid=self.kwargs.get("s_uid"), is_active=True
        ).select_related("user", "server")

    def get_serializer_context(self):
        s_uid = self.kwargs.get("s_uid")
        server = get_object_or_404(Server, uid=s_uid)
        context = super().get_serializer_context()
        context["request"] = self.request
        context["server"] = server
        return context


class MemberDetailsView(RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Member:
        member = get_object_or_404(Member, uid=self.kwargs.get("m_uid"))
        if member.server_uid != str(self.kwargs.get("s_uid")):
            raise exceptions.NotFound()
        return member


class MemberDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self) -> Member:
        mem_uid = self.kwargs.get("m_uid")
        if self.request.user.uid != mem_uid:
            raise exceptions.PermissionDenied()
        return get_object_or_404(Member, uid=mem_uid)

    def perform_destroy(self, instance: Member) -> None:
        instance.is_active = False
        instance.save()
