from django.db import models

from django.contrib.auth import get_user_model
from projectile.base.models import BaseModelWithUID, BaseModelWithSlug

User = get_user_model()


"""
IMPORTANT!!

Some Foreignkey relations might feel like they are redundant
(i.e. we have category in channel, and server in category
so we can write channel.category.server to get the server right?)
yes, but when you have 100 million instances and complex subqueries select_related helps but not that much
you can't afford 10 second long queries because you have to make join operations everytime

"""


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
    server_data = models.JSONField(default=dict, blank=True)
    channel_data = models.JSONField(default=dict, blank=True)

    # url fields
    icon_url = models.CharField(blank=True)
    banner_url = models.CharField(blank=True)

    def save(self, *args, **kwargs):
        if not self.owner:
            raise ValueError("Owner must always be set!!")
        return super().save(*args, **kwargs)


class Category(BaseModelWithSlug):
    # foreignkey fields
    server = models.ForeignKey(
        "server.Server", on_delete=models.CASCADE, related_name="categories"
    )

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


class Thread(BaseModelWithSlug):
    # foreignkey fields
    server = models.ForeignKey(
        "server.Server",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey("server.Category", on_delete=models.CASCADE)
    channel = models.ForeignKey(
        "server.Channel", on_delete=models.CASCADE, db_index=True
    )

    # model fields
    is_archived = models.BooleanField(default=False)
    auto_archive_duration = models.IntegerField(
        default=30, help_text="stays active for 30 days by default"
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

    accessible_channels = models.JSONField(default=dict, blank=True)


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
