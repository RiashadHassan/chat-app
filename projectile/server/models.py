from django.db import models

from django.contrib.auth import get_user_model
from projectile.base.models import BaseModelWithUID, BaseModelWithSlug

User = get_user_model()


class Server(BaseModelWithSlug):
    # foreignkey fields
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_index=True)

    # model fields
    is_deleted = models.BooleanField(
        default=False, help_text="has server been soft deleted by owner?"
    )
    description = models.TextField()
    user_limit = models.BigIntegerField(
        default=1000000, help_text="how many users can join this server?"
    )
    channel_data = models.JSONField(default=dict)

    # url fields
    icon_url = models.CharField(blank=True)
    banner_url = models.CharField(blank=True)


class Category(BaseModelWithSlug):
    # foreignkey fields
    server = models.ForeignKey("server.Server", on_delete=models.CASCADE)

    # model fields
    position = models.FloatField()


class Channel(BaseModelWithSlug):
    # foreignkey fields
    server = models.ForeignKey("server.Server", on_delete=models.CASCADE)
    category = models.ForeignKey("server.Category", on_delete=models.CASCADE)

    # model fields
    user_limit = models.BigIntegerField(
        default=1000000, help_text="how many users can join this channel?"
    )
    position = models.FloatField()
    is_private = models.BooleanField(default=False, help_text="is the channel private?")
    slow_mode = models.IntegerField(
        default=0, help_text="how many seconds should pass between messages?"
    )


class AuditLog(BaseModelWithUID):
    # foreignkey fields
    user = models.ForeignKey("core.User", on_delete=models.CASCADE, db_index=True)
    server = models.ForeignKey("server.Server", on_delete=models.CASCADE, db_index=True)

    # model fields
    action = models.CharField()
    details = models.TextField(blank=True)


class ServerMember(BaseModelWithUID):
    # foreignkey fields
    user = models.ForeignKey("core.User", on_delete=models.CASCADE, db_index=True)
    server = models.ForeignKey("server.Server", on_delete=models.CASCADE, db_index=True)

    accessible_channels = models.JSONField(default=dict)


# class ChannelMember(BaseModelWithUID):
#     # foreignkey fields
#     user = models.ForeignKey("core.User", on_delete=models.CASCADE, db_index=True)
#     server = models.ForeignKey("server.Server", on_delete=models.CASCADE, db_index=True)


# class ChannelAccess(BaseModelWithUID):
#     pass


# class Role(BaseModelWithSlug):
#     pass


# class ServerRole(BaseModelWithUID):
#     pass
