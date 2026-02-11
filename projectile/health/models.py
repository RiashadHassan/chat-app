import uuid

from datetime import timedelta

from django.db import models

from health.choices import (
    HealthCheckType,
    HealthStatus,
    HealthCheckClientType,
    HealthCheckClientSource,
    HealthCheckProtocol,
)

from projectile.ttl.mixins import TTLModelMixin


class HealthCheckLog(models.Model, TTLModelMixin):
    TTL_FIELD = "created_at"
    TTL_DURATION = timedelta(days=30)

    uid = models.CharField(
        max_length=36, default=uuid.uuid4, editable=False, unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the health check was performed",
    )

    check_type = models.CharField(
        max_length=20,
        choices=HealthCheckType.choices,
        default=HealthCheckType.UNKNOWN,
        help_text="Type of health check performed",
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=HealthStatus.choices,
        default=HealthStatus.UNKNOWN,
        help_text="Resulting status of the health check",
        db_index=True,
    )

    response_time_ms = models.PositiveIntegerField(
        null=True, blank=True, help_text="Time taken in milliseconds"
    )

    request_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Data sent in the health check request",
    )
    response_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Data received in the health check response",
    )

    client_type = models.CharField(
        max_length=20,
        choices=HealthCheckClientType.choices,
        default=HealthCheckClientType.UNKNOWN,
        help_text="Broad type of client performing the check",
    )
    client_source = models.CharField(
        max_length=20,
        choices=HealthCheckClientSource.choices,
        default=HealthCheckClientSource.UNKNOWN,
        help_text="Specific source of the client (e.g., Kubernetes, Load Balancer)",
    )

    protocol = models.CharField(
        max_length=10,
        choices=HealthCheckProtocol.choices,
        default=HealthCheckProtocol.UNKNOWN,
        help_text="Protocol used for the health check",
    )

    # TODO: should probably add fields for the below reasosns as well
    # a field for error details if status is UNHEALTHY
    # and possibly a field for more gunicorn/django server metrics?
    # maybe a field for whichever instance/server handled the request
    # depending on how detailed we want the logs to be

    class Meta:
        db_table = "health_check_logs"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["check_type"]),
            models.Index(fields=["client_type"]),
            models.Index(fields=["client_source"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.check_type} | {self.status} | {self.created_at}"
