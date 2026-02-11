from django.utils import timezone
from django.core.management.base import BaseCommand

from projectile.ttl import TTL_LOGGER
from projectile.ttl.manager import TTLManager
from projectile.ttl.discovery import TTLModelDiscovery
from projectile.ttl.executor import TTLDeletionExecutor
from projectile.ttl.policies import TTLCleanupPolicy


class Command(BaseCommand):
    help = "Run centralized TTL cleanup"

    def handle(self, *args, **kwargs):
        TTL_LOGGER.info(
            "Executing 'run_ttl_cleanup' management command at %s", timezone.now()
        )
        manager = TTLManager(
            discovery=TTLModelDiscovery(),
            policy=TTLCleanupPolicy(),
            executor=TTLDeletionExecutor(),
        )
        manager.run_cleanup()
