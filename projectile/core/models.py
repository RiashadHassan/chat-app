import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField

from projectile.core.choices import StatusChoices
from projectile.core.manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=120, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(
        unique=True,
    )
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.OFFLINE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now() 
        return super().save()

    def __str__(self):
        return f"{self.username} : {self.email}"


# class UserDetails(models.Model):
