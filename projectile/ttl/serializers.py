from rest_framework import serializers


class TTLModelSerializer(serializers.Serializer):
    app_label = serializers.CharField()
    model_name = serializers.CharField()
    ttl_field = serializers.CharField()
    ttl_days = serializers.IntegerField()


class TTLModelsListResponseSerializer(serializers.Serializer):
    models = TTLModelSerializer(many=True)
