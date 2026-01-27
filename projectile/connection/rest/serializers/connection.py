from rest_framework import serializers
from connection.models import UserConnection


class UserConnectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConnection
        fields = [
            "uid",
            "left_user_uid",
            "right_user_uid",
        ]
        read_only_fields = fields


class UserConnectionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConnection
        fields = [
            "uid",
            "left_user_uid",
            "right_user_uid",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields
