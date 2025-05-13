from django.db import transaction
from rest_framework import serializers

from projectile.base.dynamic_serializer import UserDynamicSerializer
from projectile.server.models import Server


class ServerListCreateSerializer(serializers.ModelSerializer):
    owner = UserDynamicSerializer(fields=("uid", "username", "status"), read_only=True)

    class Meta:
        model = Server
        fields = [
            "uid",
            "slug",
            "name",
            "owner",
            "description",
            "user_limit",
            "icon_url",
            "banner_url",
            "created_at",
        ]

        read_only = [
            "uid",
            "slug",
            "created_at",
            "updated_at",
        ]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["owner"] = user
        validated_data["server_data"] = {"owner": str(user.uid)}
        return super().create(validated_data)


class ServerRetrieveSerializer(serializers.ModelSerializer):
    owner = UserDynamicSerializer(fields=("uid", "username", "status"), read_only=True)

    class Meta:
        model = Server
        fields = [
            "uid",
            "slug",
            "name",
            "owner",
            "description",
            "user_limit",
            "icon_url",
            "banner_url",
            "server_data",
            "categories",
            "created_at",
        ]

        read_only = [
            "uid",
            "slug",
            "created_at",
            "updated_at",
        ]