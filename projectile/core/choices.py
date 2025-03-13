from django.db import models


class StatusChoices(models.TextChoices):
    ACTIVE = "active", "ACTIVE"
    INACTIVE = "inactive", "INACTIVE"
    ONLINE = "online", "ONLINE"
    OFFLINE = "offline", "OFFLINE"
    AWAY = "away", "AWAY"
    DND = "do not disturb", "DO NOT DISTURB"
