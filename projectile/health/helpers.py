import time
import logging

from django.db import connection
from django.core.cache import cache

LOGGER = logging.getLogger(__name__)


class HealthCheckHelper:
    @staticmethod
    def check_database() -> tuple[bool, int | None]:
        _start = time.monotonic()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return True, HealthCheckHelper._elapsed_ms(_start)
        except Exception as e:
            LOGGER.critical("DATABASE CONNECTION ERROR:", exc_info=e)
            return False, HealthCheckHelper._elapsed_ms(_start)

    @staticmethod
    def check_cache() -> tuple[bool, int | None]:
        _start = time.monotonic()
        try:
            cache.set("health_check", "ok", timeout=5)
            cache.get("health_check")
            return True, HealthCheckHelper._elapsed_ms(_start)

        except Exception as e:
            LOGGER.critical("CACHE CONNECTION ERROR:", exc_info=e)
            return False, HealthCheckHelper._elapsed_ms(_start)

    @staticmethod
    def _elapsed_ms(start: float) -> int:
        return int((time.monotonic() - start) * 1000)
