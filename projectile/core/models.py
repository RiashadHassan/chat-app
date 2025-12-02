import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField

from base.models import BaseModelWithSlug
from core.choices import GeneralStatusChoices, UserStatusChoices
from core.manager import CustomUserManager

from server.models import ServerSpectrum


class User(AbstractBaseUser, PermissionsMixin):
    # models fields
    uid = models.CharField(
        max_length=36, default=uuid.uuid4, editable=False, unique=True
    )
    username = models.CharField(max_length=120, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    status = models.CharField(
        choices=UserStatusChoices.choices, default=UserStatusChoices.OFFLINE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    # permission fields
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    # url_fields
    profile_pic_url = models.TextField(default="", blank=True)
    banner_url = models.TextField(default="", blank=True)

    # in order to avoid DB queries
    metadata = models.JSONField(default=dict)
    server_data = models.JSONField(default=dict)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save()

    def __str__(self):
        return f"{self.username} : {self.email}"


class Spectrum(BaseModelWithSlug):
    # model fields
    description = models.CharField(max_length=255, blank=True)
    server_count = models.BigIntegerField(default=0, blank=True, db_index=True)

    # m2m fields
    servers = models.ManyToManyField(
        to="server.Server", through="server.ServerSpectrum", related_name="spectra"
    )
    # url fields
    icon_url = models.TextField(default="", blank=True)

    class Meta:
        verbose_name_plural = "Spectra"
        ordering = ["-server_count", "name"]

    def __str__(self):
        return f"Spectrum: {self.name} - {self.server_count} servers"

    def update_server_count(self):
        self.server_count = ServerSpectrum.objects.filter(
            spectrum=self, server__is_deleted=False
        ).count()
        self.save(update_fields=["server_count"])

    @property
    def active_servers(self):
        return self.servers.filter(is_deleted=False)
