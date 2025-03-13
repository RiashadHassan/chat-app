from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, aauthenticate
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from ..serializers.user import UserRegisterSerializer
from rest_framework.response import Response

from rest_framework import status

User = get_user_model()

class UserRegisterView(CreateAPIView):
    # def post(self, *args, **kwargs):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)