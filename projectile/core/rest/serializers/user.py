from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
        }

    @transaction.atomic
    def create(self, validated_data):

        # must pop email and password for the custom create_user method
        password = validated_data.pop("password")
        email = validated_data.pop("email")

        # custom model manager
        user = User.objects.create_user(email, password, **validated_data)
        return user
