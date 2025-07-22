import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from base.permissions import IsSuperUser


class ConcurrencyAPIView(APIView):
    """
    just to check how many concurrent requests device can handle
    will work for
    gunicorn and development 'python manage.py runserver'

    trigger via ""
    """

    def get(self, request, *args, **kwargs):
        delimiter = request.query_params.get("q")
        for i in range(20):
            print(delimiter)
            # from core.models import User
            # users = User.objects.first()
            # time.sleep(0.1)
        return Response({"username": "users.username", "delimiter": delimiter})


class HealthCheckAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        return Response("Projectile Django is running!")


class GunicornHealthCheckAPIView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        time.sleep(30)
        return Response("Were you able to run other views?")
