from django.db import transaction
from rest_framework import serializers

from server.models import Role


class RoleListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "uid",
            "name",
            "color",
            "position",
            "created_by",
            "created_at",
            "updated_at",
            "icon_url",
        ]
        read_only_fields = ["uid", "created_by", "created_at", "updated_at"]

    @transaction.atomic
    def create(self, validated_data):
        validated_data["server"] = self.context["server"]
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class RoleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "uid",
            "name",
            "color",
            "position",
            "created_by",
            "created_at",
            "updated_at",
            "icon_url",
        ]
        read_only_fields = ["uid", "created_by", "created_at", "updated_at"]

    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
