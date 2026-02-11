from typing import Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from projectile.ttl import TTL_LOGGER
from projectile.ttl.discovery import TTLModelDiscovery
from projectile.ttl.services import TTLIntrospectionService
from projectile.ttl.serializers import TTLModelsListResponseSerializer


class TTLModelsListView(APIView):
    """
    Read-only endpoint exposing TTL-enabled models
    NOT intended for public use EVER
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args: Any, **kwargs: Any) -> Response:
        user_id = request.user.id

        TTL_LOGGER.info(
            "TTL model introspection requested by user %s (path: %s)",
            user_id,
            request.path,
        )

        service = TTLIntrospectionService(discovery=TTLModelDiscovery())
        models = service.list_ttl_models()

        serializer = TTLModelsListResponseSerializer(instance={"models": models})

        TTL_LOGGER.info(
            "TTL model introspection completed - found %d models",
            len(models),
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
