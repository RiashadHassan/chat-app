from django.db import models


class ConnectionRequestStatus(models.TextChoices):
    PENDING = "pending", "PENDING"
    ACCEPTED = "accepted", "ACCEPTED"
    REJECTED = "rejected", "REJECTED"
    CANCELLED = "cancelled", "CANCELLED"
