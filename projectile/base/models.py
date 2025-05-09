import uuid
from django.utils import timezone
from django.db import models
from autoslug import AutoSlugField


class BaseModelWithUID(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save()


class BaseModelWithSlug(BaseModelWithUID):
    name = models.CharField(max_length=128)
    slug = AutoSlugField(populate_from="name", unique=True, editable=False)

    class Meta:
        abstract = True
