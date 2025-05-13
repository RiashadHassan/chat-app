from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from ..serializers.user import UserRegisterSerializer, UserRetrieveUpdateSerializer

User = get_user_model()


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = "uid"
    lookup_url_kwarg = "uid"


class PrivateUserManageView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer

    def get_object(self):
        return get_object_or_404(User, uid=self.request.user.uid)


class PrivateUserDestroyView(DestroyAPIView):
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, uid=self.request.user.uid)
