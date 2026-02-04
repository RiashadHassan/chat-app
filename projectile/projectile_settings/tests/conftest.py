from django.core.management import call_command
from django.test import TestCase

from projectile.projectile_settings.utils import SystemUtils


class SystemConfTestCase(TestCase):
    """
    Base test case for system-level configuration tests
    Ensures that an in-memory SQLite database has migrations applied
    before running any tests that depend on database tables
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # only run migrations if using in-memory SQLite
        if SystemUtils.get_db_vendor() == "sqlite":
            call_command("migrate", verbosity=0, interactive=False)

    def test_db_vendor_is_sqlite(self):
        engine = SystemUtils.get_db_vendor()
        self.assertEqual(engine, "sqlite")
