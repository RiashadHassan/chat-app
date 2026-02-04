from django.db import connection


class SystemUtils:
    """
    Utility class for system-level operations related to database and settings
    All methods are static and independent of instance state
    """

    @staticmethod
    def get_db_vendor() -> str:
        """
        Returns the current database vendor Django is using
        should return 'sqlite' for tests and 'postgresql' otherwise
        """
        return connection.vendor
