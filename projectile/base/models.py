import uuid
from django.utils import timezone
from django.db import models
from autoslug import AutoSlugField

"""uid = models.UUID needs to be converted to string in every scenario,
hence: uid = models.CharField() """


class BaseModelWithUID(models.Model):
    uid = models.CharField(
        max_length=36, default=uuid.uuid4, editable=False, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True

    def update_uids(self):
        for field in self._meta.fields:
            if isinstance(field, models.ForeignKey):
                attr = f"{field.name}_uid"
                if hasattr(self, attr):
                    setattr(self, attr, getattr(getattr(self, field.name), "uid", None))

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.update_uids()
        return super().save()


class BaseModelWithSlug(BaseModelWithUID):
    name = models.CharField(max_length=128, db_index=True)
    slug = AutoSlugField(populate_from="name", unique=True, editable=False)

    class Meta:
        abstract = True
