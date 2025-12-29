from rest_framework import serializers, exceptions
from rest_framework.generics import get_object_or_404

from django.http import Http404

from core.models import User

from connection.choices import ConnectionRequestStatus
from connection.models import ConnectionRequest


class ConnectionRequestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = [
            "uid",
            "sender_uid",
            "receiver_uid",
            "status",
            "created_at",
            "updated_at",
            "rejected_at",
        ]

        read_only_fields = fields


class ConnectionRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = ["receiver_uid"]

    def validate(self, attrs):
        try:
            sender = self.context["request"].user
            receiver_uid = attrs.pop("receiver_uid")

            if sender.uid == receiver_uid:
                raise serializers.ValidationError("Cannot send request to this user.")

            receiver = User.objects.get(uid=receiver_uid)

            if ConnectionRequest.objects.filter(
                sender=sender,
                receiver=receiver,
                status=ConnectionRequestStatus.PENDING,
            ).exists():
                raise serializers.ValidationError("Cannot send request to this user.")

            attrs["sender"] = sender
            attrs["receiver"] = receiver
            return attrs

        except User.DoesNotExist:
            raise Http404("No %s matches the given query." % User._meta.object_name)
