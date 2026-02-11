from django.utils import timezone
from django.db.models import Model, QuerySet


class TTLCleanupPolicy:
    """TTL cutoff calculations"""

    def get_queryset(self, model: Model) -> QuerySet:
        cutoff = self._get_cutoff(model=model)
        return model.objects.filter(**{f"{model.TTL_FIELD}__lt": cutoff})

    def _get_cutoff(self, model: Model):
        return timezone.now() - model.TTL_DURATION
