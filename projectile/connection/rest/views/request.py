from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404

from core.models import User

from connection.models import ConnectionRequest
from connection.choices import ConnectionRequestStatus
from connection.rest.serializers.request import (
    ConnectionRequestListSerializer,
    ConnectionRequestCreateSerializer,
)


class ConnectionRequestListView(ListAPIView):
    serializer_class = ConnectionRequestListSerializer

    def get_queryset(self):
        return ConnectionRequest.objects.filter(
            status=ConnectionRequestStatus.PENDING,
            sender_uid=self.request.user.uid,
        )


class ConnectionRequestCreateView(CreateAPIView):
    serializer_class = ConnectionRequestCreateSerializer
