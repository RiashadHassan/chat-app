from django.db.models import QuerySet

from rest_framework.pagination import PageNumberPagination

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from projectile.base.permissions import IsSuperUser
from projectile.core.models import User

from projectile.core.rest.serializers.user import UserDetailsSerializer

from ..serializers.user import UserListSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsSuperUser]
    pagination_class = PageNumberPagination

    def get_queryset(self) -> QuerySet[User]:
        query_params = self.request.query_params
        deleted_only = query_params.get("deleted_only", "")

        active_only = query_params.get("active_only", "")

        if deleted_only.lower() == "true":
            return self.queryset.filter(is_deleted=True)

        if active_only.lower() == "true":
            return self.queryset.filter(is_deleted=False)

        return self.queryset


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "user_uid"
    permission_classes = [IsSuperUser]

    def get_queryset(self) -> QuerySet[User]:
        if self.request.method == "DELETE":
            return self.queryset.filter(is_deleted=False)
        return self.queryset

    def perform_destroy(self, instance: User) -> None:
        instance.is_deleted = True
        instance.save()
