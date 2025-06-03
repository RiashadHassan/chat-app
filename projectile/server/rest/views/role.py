from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from projectile.server.models import Server, Role, RolePermission
from ..serializers.role import RoleListCreateSerializer, RoleDeatailsSerializer


class RoleListCreateView(ListCreateAPIView):
    queryset = Role.objects.filter(is_deleted=False)
    serializer_class = RoleListCreateSerializer


class RoleDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.filter(is_deleted=False)
    serializer_class = RoleDeatailsSerializer
