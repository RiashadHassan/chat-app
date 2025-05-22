from django.db import transaction

from rest_framework import serializers

from projectile.base.dynamic_serializer import ServerDynamicSerializer
from projectile.member.models import Member


class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = []

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        server = self.context["server"]
        try:
            member = Member.objects.get(user_uid=user.uid, server_uid=server.uid)
            if not member.is_active:
                member.is_active = True
                member.save()
        except Member.DoesNotExist:
            validated_data["user"] = user
            validated_data["server"] = server
            member = super().create(validated_data)
        return member


class MemberListSerializer(serializers.ModelSerializer):
    # server = ServerDynamicSerializer(fields=("uid", "name"), read_only=True)

    class Meta:
        model = Member
        fields = ["uid", "user_uid", "server_uid"]


class MemberDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["uid", "is_active", "accessible_channels"]
        read_only_fields = fields
