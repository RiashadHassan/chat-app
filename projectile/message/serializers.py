from rest_framework import serializers

from message.models import Message


class ChatLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "uid",
            "author_uid",
            "channel_uid",
            "thread_uid",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
