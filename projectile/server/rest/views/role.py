from typing import Dict, Any

from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from projectile.base.permissions import OrPermission

from projectile.server.permissions import IsOwner, IsMember
from projectile.server.models import Server, Role
from ..serializers.role import RoleListCreateSerializer, RoleDetailsSerializer


class RoleListCreateView(ListCreateAPIView):
    serializer_class = RoleListCreateSerializer
    permission_classes = [OrPermission(IsAuthenticated, IsMember, IsOwner)]

    def get_queryset(self) -> QuerySet[Role]:
        return Role.objects.filter(
            is_deleted=False, server_uid=self.server_uid
        ).select_related("server", "created_by")

    def get_serializer_context(self) -> Dict[str, Any]:
        context = super().get_serializer_context()
        # only needed in create() method of the serializer
        if self.request.method == "POST":
            context["server"] = self.get_server()
        return context

    def get_server(self) -> Server:
        if not hasattr(self, "_server"):
            self._server = get_object_or_404(Server, uid=self.server_uid)
        return self._server

    @property
    def server_uid(self):
        return self.kwargs.get("server_uid")


class RoleDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoleDetailsSerializer
    permission_classes = [OrPermission(IsAuthenticated, IsMember, IsOwner)]

    def get_queryset(self) -> QuerySet[Role]:
        return Role.objects.filter(
            is_deleted=False, server_uid=self.kwargs.get("server_uid")
        ).select_related("server", "created_by")

    def get_object(self) -> Role:
        return get_object_or_404(self.get_queryset(), uid=self.kwargs.get("role_uid"))
