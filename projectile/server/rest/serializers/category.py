from django.db import transaction
from rest_framework import serializers

from projectile.server.models import Category


class CateogryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
