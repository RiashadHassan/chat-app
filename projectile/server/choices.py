from django.db import models


class ChannelTypes(models.TextChoices):
    TEXT = "text", "Text"
    VOICE = "voice", "Voice"