from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)

from projectile.server.models import Category
from ..serializers.category import CateogryListCreateSerializer


class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CateogryListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        server_uid = self.kwargs.get("server_uid")
        return Category.objects.filter(server_uid=server_uid).select_related("server")
