from rest_framework import serializers

from core.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "created_at",
            "updated_at",
        ]

        read_only_fields = fields
