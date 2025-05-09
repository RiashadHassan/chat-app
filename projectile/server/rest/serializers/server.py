from rest_framework import serializers

from projectile.base.dynamic_serializer import DynamicUserSerializer
from projectile.server.models import Server


class ServerListCreateSerializer(serializers.ModelSerializer):
    owner = DynamicUserSerializer(fields=("username", "status"), read_only=True)

    class Meta:
        model = Server
        fields = [
            "name",
            "slug",
            "owner",
            "description",
            "user_limit",
            "icon_url",
            "banner_url",
            "created_at",
        ]

        read_only = [
            "slug",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)