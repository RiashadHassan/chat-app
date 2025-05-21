from django.db import models

from projectile.base.models import BaseModelWithSlug


class Permission(BaseModelWithSlug):
    description = models.TextField(null=True, blank=True)
