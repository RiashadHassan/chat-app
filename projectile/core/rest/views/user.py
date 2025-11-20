from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
)

from core.models import User

from ..serializers.user import UserRegisterSerializer, UserDetailsSerializer


# PUBLIC VIEW
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class LoginView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        from django.shortcuts import render
        return render(request, "login.html")


# PRIVATE USER VIEWS (FOR OWN PROFILE)
class PrivateUserDetailsView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user


class PrivateUserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self) -> User:
        return self.request.user

    def perform_destroy(self, instance) -> None:
        instance.is_deleted = True
        instance.save()
