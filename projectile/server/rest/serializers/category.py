from django.db import transaction
from rest_framework import serializers

from projectile.base.dynamic_serializer import UserDynamicSerializer
from projectile.server.models import Category


class CateogryListCreateSerializer(serializers.ModelSerializer):
    # owner = UserDynamicSerializer(fields=("uid", "username", "status"), read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        