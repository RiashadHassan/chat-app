from typing import Optional
from django.db.models import QuerySet

from projectile.ttl import TTL_LOGGER
from projectile.ttl.discovery import TTLModelDiscovery
from projectile.ttl.executor import TTLDeletionExecutor
from projectile.ttl.policies import TTLCleanupPolicy


class TTLManager:
    """Coordinates TTL discovery, cleanup-policy and execution"""

    def __init__(
        self,
        discovery: Optional[TTLModelDiscovery] = None,
        policy: Optional[TTLCleanupPolicy] = None,
        executor: Optional[TTLDeletionExecutor] = None,
    ) -> None:
        self._discovery = discovery or TTLModelDiscovery()
        self._policy = policy or TTLCleanupPolicy()
        self._executor = executor or TTLDeletionExecutor()

    def run_cleanup(self) -> None:
        """Run TTL cleanup for all discovered models"""

        TTL_LOGGER.info("Starting centralized TTL cleanup run via TTLManager")

        for model in self._discovery.get_ttl_models():
            model_label = model._meta.label
            ttl_duration = str(model.TTL_DURATION)

            try:
                TTL_LOGGER.info(
                    "Running TTL cleanup for %s (TTL duration: %s)",
                    model_label,
                    ttl_duration,
                )

                # filter the queryset to delete
                queryset: QuerySet = self._policy.get_queryset(model=model)

                # execute the deletion process
                deleted_count = self._executor.execute(queryset=queryset)

                TTL_LOGGER.info(
                    "Completed TTL cleanup for %s: deleted %d rows (TTL duration: %s)",
                    model_label,
                    deleted_count,
                    ttl_duration,
                )

            except Exception as e:
                TTL_LOGGER.exception(
                    "Error running TTL cleanup for %s: %s",
                    model_label,
                    str(e),
                )

        TTL_LOGGER.info("Completed centralized TTL cleanup run")
