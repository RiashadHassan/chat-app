from rest_framework import serializers

from projectile.server.models import Role


class RoleListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = fields

class RoleDeatailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = fields
