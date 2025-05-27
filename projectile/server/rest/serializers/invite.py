from rest_framework import serializers, generics

from projectile.server.models import Server, Invite


class InviteListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = [
            "code",
            "uses",
            "max_uses",
            "inviter_uid",
            "expires_at",
        ]
        read_only_fields = fields
