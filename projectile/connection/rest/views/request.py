from datetime import timezone

from django.db.models import QuerySet


from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)


from connection.models import ConnectionRequest
from connection.choices import ConnectionRequestStatus
from connection.rest.serializers.request import (
    ConnectionRequestListSerializer,
    ConnectionRequestCreateSerializer,
)


# SENT REQUEST VIEWS
class ConnectionRequestCreateView(CreateAPIView):
    serializer_class = ConnectionRequestCreateSerializer


class SentConnectionRequestListView(ListAPIView):
    serializer_class = ConnectionRequestListSerializer

    def get_queryset(self) -> QuerySet[ConnectionRequest]:
        return ConnectionRequest.objects.filter(
            status=ConnectionRequestStatus.PENDING,
            sender_uid=self.request.user.uid,
        )


class SentConnectionRequestDetailsView(RetrieveAPIView):
    serializer_class = ConnectionRequestListSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "request_uid"

    def get_queryset(self) -> QuerySet[ConnectionRequest]:
        user_uid = self.request.user.uid
        return ConnectionRequest.objects.filter(sender_uid=user_uid)


class CancelConnectionRequestView(DestroyAPIView):
    """View for cancelling outgoing connection requests"""

    serializer_class = ConnectionRequestListSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "request_uid"

    def get_queryset(self) -> QuerySet[ConnectionRequest]:
        return ConnectionRequest.objects.filter(
            status=ConnectionRequestStatus.PENDING,
            sender_uid=self.request.user.uid,
        )

    def perform_destroy(self, instance: ConnectionRequest) -> None:
        instance.status = ConnectionRequestStatus.CANCELLED
        instance.save()


# RECEIVED REQUEST VIEWS
class ReceivedConnectionRequestListView(ListAPIView):
    serializer_class = ConnectionRequestListSerializer

    def get_queryset(self) -> QuerySet[ConnectionRequest]:
        return ConnectionRequest.objects.filter(
            status=ConnectionRequestStatus.PENDING,
            receiver_uid=self.request.user.uid,
        )


class ReceivedConnectionRequestDetailsView(RetrieveAPIView):
    serializer_class = ConnectionRequestListSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "request_uid"

    def get_queryset(self) -> QuerySet[ConnectionRequest]:
        return ConnectionRequest.objects.filter(receiver_uid=self.request.user.uid)


class RejectConnectionRequestView(DestroyAPIView):
    """View for rejecting incoming connection requests"""

    serializer_class = ConnectionRequestListSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "request_uid"

    def get_queryset(self) -> QuerySet[ConnectionRequest]:
        return ConnectionRequest.objects.filter(
            status=ConnectionRequestStatus.PENDING,
            receiver_uid=self.request.user.uid,
        )

    def perform_destroy(self, instance: ConnectionRequest) -> None:
        instance.status = ConnectionRequestStatus.REJECTED
        instance.rejected_at = timezone.now()
        instance.save()


class AcceptConnectionRequestView(UpdateAPIView):
    serializer_class = ConnectionRequestListSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "request_uid"

    def get_queryset(self) -> QuerySet[ConnectionRequest]:
        return ConnectionRequest.objects.filter(
            status=ConnectionRequestStatus.PENDING,
            receiver_uid=self.request.user.uid,
        )

    def perform_update(self, serializer) -> None:
        # passing as kwarg into the save method of 'serializers.BaseSerializer'
        # there it will merge the 'kwargs' and the 'validated_data' dict
        # then it will update the model instance with the merged data
        serializer.save(status=ConnectionRequestStatus.ACCEPTED)
