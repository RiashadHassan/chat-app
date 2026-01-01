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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag, not actually deleted from the database.",
        db_index=True,
    )

    class Meta:
        abstract = True

    def update_uids(self):
        for field in self._meta.fields:
            if isinstance(field, models.ForeignKey):
                attr = f"{field.name}_uid"
                if hasattr(self, attr):
                    fk_obj = getattr(self, field.name)
                    # If the foreign key object is None, set the uid to an empty string
                    # setting it to None may cause issues since uid is defined as CharField
                    # and null = True is not set.
                    uid_value = getattr(fk_obj, "uid", "")
                    setattr(self, attr, str(uid_value))

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        self.update_uids()
        return super().save()

    def __str__(self):
        # should never be triggered. child models should always override this method.
        return f"{self._meta.model_name}: {getattr(self, 'uid', super().__str__())}"


class BaseModelWithSlug(BaseModelWithUID):
    name = models.CharField(max_length=128, db_index=True)
    slug = AutoSlugField(populate_from="name", unique=True, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        # should never be triggered. child models should always override this method.
        return f"{self._meta.model_name}: {getattr(self, 'name', super().__str__())}"
