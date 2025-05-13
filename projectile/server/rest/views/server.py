from rest_framework.views import APIView
from rest_framework.generics import (
    get_object_or_404,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import AllowAny, IsAuthenticated

from projectile.base.permissions import IsSuperUser
from projectile.server.models import Server
from projectile.server.permissions import IsOwner

from projectile.server.rest.serializers.server import (
    ServerListCreateSerializer,
    ServerRetrieveSerializer,
)


class ServerListCreateView(ListCreateAPIView):
    queryset = Server.objects.filter(is_deleted=False)
    serializer_class = ServerListCreateSerializer

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]  # so that anyone can access the server list
        return super().get_permissions()

    # def get_queryset(self):
    # if self.request.query_params.get("all_servers", None):
    #     return Server.objects.all()
    # return self.queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ServerRetrieveView(RetrieveAPIView):
    queryset = Server.objects.filter(is_deleted=False).prefetch_related("categories")
    serializer_class = ServerRetrieveSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"


class ServerUpdateView(UpdateAPIView):
    queryset = Server.objects.filter(is_deleted=False)
    serializer_class = ServerRetrieveSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    permission_classes = [IsOwner]

class ServerDestroyView(DestroyAPIView):
    queryset = Server.objects.filter(is_deleted=False)
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    permission_classes = [IsOwner]

    def get_object(self):
        uid = self.kwargs.get("uid")
        return get_object_or_404(Server, uid=uid)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
