from rest_framework import serializers


class ServerSearchSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    name = serializers.CharField()
    slug = serializers.SlugField()
    description = serializers.CharField()
    is_deleted = serializers.BooleanField()
    owner_uid = serializers.CharField()
    owner_username = serializers.CharField()
