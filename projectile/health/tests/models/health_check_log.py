from django.test import TestCase
from django.db import IntegrityError, transaction

from health.models import HealthCheckLog
from health.choices import (
    HealthCheckType,
    HealthStatus,
    HealthCheckClientType,
    HealthCheckClientSource,
    HealthCheckProtocol,
)


class HealthCheckLogModelTest(TestCase):
    def setUp(self):
        super().setUp()
        self.default_kwargs = {
            "check_type": HealthCheckType.UNKNOWN,
            "status": HealthStatus.UNKNOWN,
            "client_type": HealthCheckClientType.UNKNOWN,
            "client_source": HealthCheckClientSource.UNKNOWN,
            "protocol": HealthCheckProtocol.UNKNOWN,
        }

    def test_create_health_check_log_success(self):
        log = HealthCheckLog.objects.create(**self.default_kwargs)
        self.assertIsInstance(log, HealthCheckLog)

    def test_uid_is_generated(self):
        log = HealthCheckLog.objects.create(**self.default_kwargs)
        self.assertIsNotNone(log.uid)

    def test_created_at_is_set(self):
        log = HealthCheckLog.objects.create(**self.default_kwargs)
        self.assertIsNotNone(log.created_at)

    def test_default_field_values(self):
        log = HealthCheckLog.objects.create(**self.default_kwargs)

        self.assertEqual(log.check_type, HealthCheckType.UNKNOWN)
        self.assertEqual(log.status, HealthStatus.UNKNOWN)
        self.assertEqual(log.client_type, HealthCheckClientType.UNKNOWN)
        self.assertEqual(log.client_source, HealthCheckClientSource.UNKNOWN)
        self.assertEqual(log.protocol, HealthCheckProtocol.UNKNOWN)
        self.assertEqual(log.request_data, {})
        self.assertEqual(log.response_data, {})
        self.assertIsNone(log.response_time_ms)

    def test_string_representation(self):
        log = HealthCheckLog.objects.create(**self.default_kwargs)
        expected = f"{log.check_type} | {log.status} | {log.created_at}"
        self.assertEqual(str(log), expected)

    def test_optional_response_time(self):
        log = HealthCheckLog.objects.create(**self.default_kwargs, response_time_ms=123)
        self.assertEqual(log.response_time_ms, 123)

    def test_unique_uid_constraint(self):
        log1 = HealthCheckLog.objects.create(**self.default_kwargs)

        with self.assertRaises(IntegrityError):
            HealthCheckLog.objects.create(**self.default_kwargs, uid=log1.uid)

    def test_not_null_constraints(self):
        """
        Only test fields that are logically required and non-nullable
        """
        non_nullable_fields = [
            "check_type",
            "status",
            "client_type",
            "client_source",
            "protocol",
        ]

        for field in non_nullable_fields:
            with self.subTest(field=field):
                log = HealthCheckLog.objects.create(**self.default_kwargs)
                # updating non-nullable fields to 'None' should raise IntegrityError
                try:
                    # wrap in transaction to avoid TransactionManagementError
                    # in 'django.test.TestCase', simpler than a separate 'TransactionTestCase'
                    with transaction.atomic():
                        setattr(log, field, None)
                        log.save()
                except IntegrityError:
                    pass

                log.refresh_from_db()
                self.assertIsNotNone(getattr(log, field))
                log.delete()

    def test_ordering_by_created_at_desc(self):
        log1 = HealthCheckLog.objects.create(**self.default_kwargs)
        log2 = HealthCheckLog.objects.create(**self.default_kwargs)

        logs = list(HealthCheckLog.objects.all())
        self.assertEqual(logs[0], log2)
        self.assertEqual(logs[1], log1)

    def test_indexes_exist(self):
        """
        Ensure model Meta indexes are defined as expected.
        """
        index_fields = {tuple(index.fields) for index in HealthCheckLog._meta.indexes}

        expected_indexes = {
            ("created_at",),
            ("status",),
            ("check_type",),
            ("client_type",),
            ("client_source",),
        }

        self.assertEqual(index_fields, expected_indexes)
