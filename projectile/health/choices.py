from django.db import models


class HealthCheckType(models.TextChoices):
    HEALTH = "health", "HEALTH"
    READINESS = "readiness", "READINESS"
    LIVENESS = "liveness", "LIVENESS"
    UNKNOWN = "unknown", "UNKNOWN"


class HealthStatus(models.TextChoices):
    HEALTHY = "healthy", "HEALTHY"
    UNHEALTHY = "unhealthy", "UNHEALTHY"
    DEGRADED = "degraded", "DEGRADED"
    UNKNOWN = "unknown", "UNKNOWN"


class HealthCheckClientType(models.TextChoices):
    INTERNAL = "internal", "INTERNAL"
    EXTERNAL = "external", "EXTERNAL"
    THIRD_PARTY = "third_party", "THIRD PARTY"
    UNKNOWN = "unknown", "UNKNOWN"


class HealthCheckClientSource(models.TextChoices):
    KUBERNETES = "kubernetes", "KUBERNETES"
    LOAD_BALANCER = "load_balancer", "LOAD BALANCER"
    MONITORING = "monitoring", "MONITORING"
    MANUAL = "manual", "MANUAL"
    BROWSER = "browser", "BROWSER"
    UNKNOWN = "unknown", "UNKNOWN"


class HealthCheckProtocol(models.TextChoices):
    HTTP = "http", "HTTP"
    HTTPS = "https", "HTTPS"
    UNKNOWN = "unknown", "UNKNOWN"
