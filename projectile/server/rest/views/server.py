from typing import List
from django.db.models import Prefetch, QuerySet

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import BasePermission, AllowAny, IsAuthenticated

from server.models import Server, Category
from server.permissions import IsOwner, IsMember, IsMemberCached

from server.rest.serializers.server import (
    ServerListCreateSerializer,
    ServerDetailsSerializer,
)


class ServerListCreateView(ListCreateAPIView):
    serializer_class = ServerListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  # so that anyone can access the server list
        return super().get_permissions()

    def get_queryset(self) -> QuerySet[Server]:
        return Server.objects.filter(is_deleted=False).select_related("owner")


class ServerDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = ServerDetailsSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "server_uid"

    def get_permissions(self) -> List[BasePermission]:
        if self.request.method == "GET":
            return [IsMemberCached(), IsMember()]
        return [IsOwner()]

    def get_queryset(self) -> QuerySet[Server]:
        active_categories = Prefetch(
            "categories",
            queryset=(Category.objects.filter(is_deleted=False)),
        )
        queryset = (
            Server.objects.filter(is_deleted=False)
            .prefetch_related(active_categories)
            .select_related("owner")
        )
        return queryset

    def perform_destroy(self, instance: Server) -> None:
        if not instance.is_deleted:
            instance.is_deleted = True
            instance.save()
