from django.utils import timezone
from django.core.management.base import BaseCommand

from ttl import TTL_LOGGER
from ttl.manager import TTLManager
from ttl.discovery import TTLModelDiscovery
from ttl.executor import TTLDeletionExecutor
from ttl.policies import TTLCleanupPolicy


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
