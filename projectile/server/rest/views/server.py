from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.permissions import IsAuthenticated

from projectile.server.models import Server

from projectile.server.rest.serializers.server import ServerListCreateSerializer


class ServerListCreateView(ListCreateAPIView):
    queryset = Server.objects.filter()
    serializer_class = ServerListCreateSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.query_params.get("all=True"):
            return self.queryset.filter(is_deleted=False)
        return self.queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
