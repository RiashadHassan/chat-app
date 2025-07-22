from django.db import transaction

from rest_framework import serializers

from member.models import Member


class MemberListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["uid", "user_uid", "server_uid"]
        read_only_fields = ["uid", "user_uid", "server_uid"]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        server = self.context["server"]
        try:
            member = Member.objects.get(user=user, server=server)
            if member.is_deleted:
                member.is_deleted = False
                member.save()
        except Member.DoesNotExist:
            validated_data["user"] = user
            validated_data["server"] = server
            member = super().create(validated_data)
        return member


class MemberDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["uid", "is_deleted", "accessible_channels"]
        read_only_fields = fields
