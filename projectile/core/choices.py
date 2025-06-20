from django.db import models


class GeneralStatusChoices(models.TextChoices):
    ACTIVE = "active", "ACTIVE"
    INACTIVE = "inactive", "INACTIVE"
    ARCHIVED = "archived", "ARCHIVED"
    OTHER = "other", "OTHER"


class UserStatusChoices(models.TextChoices):
    ACTIVE = "active", "ACTIVE"
    INACTIVE = "inactive", "INACTIVE"
    ONLINE = "online", "ONLINE"
    OFFLINE = "offline", "OFFLINE"
    AWAY = "away", "AWAY"
    DND = "do not disturb", "DO NOT DISTURB"
