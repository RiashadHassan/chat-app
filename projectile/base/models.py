import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from autoslug import AutoSlugField

class BaseModelWithUID(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, force_insert=..., force_update=..., using=..., update_fields=...):
        self.updated_at = timezone.now()
        return super().save(force_insert, force_update, using, update_fields)
    
class BaseModelWithSlug(BaseModelWithUID):
    slug = AutoSlugField(populate_from="name", unique=True, editable=False)

    class Meta:
        abstract = True