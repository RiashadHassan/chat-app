from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
)

from projectile.base.permissions import IsSuperUser
from projectile.core.models import User

from ..serializers.user import (
    UserRegisterSerializer,
    UserRetrieveUpdateSerializer,
    UserListSerializer,
)


# PUBLIC VIEW
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


# PRIVATE USER VIEWS (FOR OWN PROFILE)
class PrivateUserDetailsView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
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


# ADMIN VIEWS WHERE SYSTEM ADMINS CAN ACCESS USER PROFILES
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self) -> QuerySet[User]:
        query_params = self.request.query_params
        deleted_only = query_params.get("deleted_only", "")

        active_only = query_params.get("active_only", "")

        if deleted_only.lower() == "true":
            return self.queryset.filter(is_deleted=True)

        if active_only.lower() == "true":
            return self.queryset.filter(is_deleted=False)

        return self.queryset


class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    permission_classes = [IsSuperUser]


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.filter(is_deleted=False)
    lookup_field = "uid"
    lookup_url_kwarg = "uid"
    permission_classes = [IsSuperUser]

    def perform_destroy(self, instance) -> None:
        instance.is_deleted = True
        instance.save()
