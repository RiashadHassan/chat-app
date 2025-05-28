from django.db import transaction
from rest_framework import serializers

from projectile.base.dynamic_serializer import (
    ChannelDynamicSerializer,
    ThreadDynamicSerializer,
)
from projectile.server.models import Category


class CateogryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CateogryDetailsSerializer(serializers.ModelSerializer):
    # channel_count = serializers.IntegerField()
    # thread_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = [
            "uid",
            "slug",
            "name",
            # "channel_count",
            # "thread_count",
        ]
