from django.core.cache import cache

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from base.cache_keys import HEALTH_CHECK_CACHE_KEY, LIVENESS_PROBE_KEY, READINESS_KEY

from health.helpers import HealthCheckHelper
from health.utils import HealthCheckUtils


class HealthCheckView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        cached_data = cache.get(HEALTH_CHECK_CACHE_KEY)
        if cached_data:
            # mark response as cached
            response_data = cached_data["data"].copy()
            response_data["cached_response"] = True
            return Response(response_data, status=cached_data["status"])

        db_ok, db_time = HealthCheckHelper.check_database()
        cache_ok, cache_time = HealthCheckHelper.check_cache()

        if not db_ok:
            data = {"status": "unhealthy", "database": "disconnected"}
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        else:
            data = {
                "status": "healthy",
                "database": {
                    "status": "connected",
                    "response_time_ms": db_time,
                },
                "cache": {
                    "status": "connected" if cache_ok else "disconnected",
                    "response_time_ms": cache_time,
                },
            }
            status_code = status.HTTP_200_OK

        data["cached_response"] = False  # mark response as not from cache
        cache.set(
            HEALTH_CHECK_CACHE_KEY, {"data": data, "status": status_code}, timeout=30
        )
        return Response(data, status=status_code)


class LivenessProbeView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        cached_data = cache.get(LIVENESS_PROBE_KEY)
        if cached_data:
            response_data = cached_data["data"].copy()
            response_data["cached_response"] = True
            return Response(response_data, status=cached_data["status"])

        data = {"status": "alive", "cached_response": False}
        status_code = status.HTTP_200_OK

        cache.set(LIVENESS_PROBE_KEY, {"data": data, "status": status_code}, timeout=10)
        return Response(data, status=status_code)


class ReadinessProbeView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        cached_data = cache.get(READINESS_KEY)
        if cached_data:
            response_data = cached_data["data"].copy()
            response_data["cached_response"] = True
            return Response(response_data, status=cached_data["status"])

        db_ok, _ = HealthCheckHelper.check_database()

        if not db_ok:
            data = {"status": "not_ready"}
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        else:
            data = {"status": "ready"}
            status_code = status.HTTP_200_OK

        data["cached_response"] = False
        cache.set(READINESS_KEY, {"data": data, "status": status_code}, timeout=10)
        return Response(data, status=status_code)
