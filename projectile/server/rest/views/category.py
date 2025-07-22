from django.db.models import Prefetch, Count, Subquery, Value, Q

from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
)


from server.models import Category, Channel, Thread
from server.permissions import IsOwner
from ..serializers.category import (
    CateogryListCreateSerializer,
    CateogryDetailsSerializer,
)


class CategoryListCreateView(ListCreateAPIView):
    serializer_class = CateogryListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        server_uid = self.kwargs.get("server_uid")
        return Category.objects.filter(server_uid=server_uid).select_related("server")


class CategoryDetailsView(RetrieveUpdateAPIView):
    serializer_class = CateogryDetailsSerializer
    permission_classes = [IsOwner]
    lookup_field = "uid"
    lookup_url_kwarg = "category_uid"

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False) #.select_related("server")

    def get_object(self):
        queryset = self.get_queryset()
        try:
            server_uid = self.kwargs.get("server_uid")
            category_uid = self.kwargs.get("category_uid")
            category = queryset.get(uid=category_uid, server_uid=server_uid)
            return category
        except Category.DoesNotExist:
            return exceptions.NotFound(detail="Category does not exist.")
