from django.db import transaction
from django.db.models import Model, QuerySet
from projectile.ttl import TTL_LOGGER


class TTLDeletionExecutor:
    """Executes TTL deletion in batches"""

    def __init__(self, batch_size: int = 10_000):
        self.batch_size = batch_size

    def execute(self, queryset: QuerySet) -> int:
        """Deletes rows from the queryset in batches"""
        model: Model = queryset.model
        total_deleted: int = 0
        batch_num: int = 1

        while True:
            ids_batch = list(
                queryset.order_by("pk").values_list("pk", flat=True)[: self.batch_size]
            )

            if not ids_batch:
                break

            with transaction.atomic():
                deleted, _ = model.objects.filter(pk__in=ids_batch).delete()
                total_deleted += deleted

                TTL_LOGGER.info(
                    "Deleted batch %d of %s: batch_size=%d, deleted=%d, total so far=%d",
                    batch_num,
                    model._meta.label,
                    len(ids_batch),
                    deleted,
                    total_deleted,
                )
            batch_num += 1
        return total_deleted
