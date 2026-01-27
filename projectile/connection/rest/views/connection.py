from django.db.models import Q, QuerySet
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from connection.models import UserConnection

from connection.rest.serializers.connection import (
    UserConnectionListSerializer,
    UserConnectionDetailsSerializer,
)


class UserConnectionListView(ListAPIView):
    serializer_class = UserConnectionListSerializer

    def get_queryset(self) -> QuerySet[UserConnection]:
        return UserConnection.objects.get_user_connections(self.request.user.uid)


class UserConnectionDetailsView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserConnectionDetailsSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"

    def get_queryset(self) -> QuerySet[UserConnection]:
        return UserConnection.objects.get_user_connections(self.request.user.uid)

    def perform_destroy(self, instance: UserConnection):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
