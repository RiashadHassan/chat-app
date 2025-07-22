from django.db import models
from django.utils import timezone

from base.models import BaseModelWithUID, BaseModelWithSlug

from server.choices import ChannelTypes

"""
IMPORTANT!!

Some Foreignkey relations might feel like they are redundant
(i.e. we have category in channel, and server in category
so we can write channel.category.server to get the server right?) yes, but
when you have 100 million rows and complex subqueries select_related helps but not that much
you can't afford 10 second long queries because you have to make join operations everytime

"""


class ServerSpectrum(BaseModelWithUID):
    # foreignkey fields
    spectrum = models.ForeignKey(
        "core.Spectrum", on_delete=models.PROTECT, related_name="spectrum_links"
    )
    spectrum_uid = models.CharField(max_length=36, db_index=True, blank=True)
    server = models.ForeignKey(
        "server.Server", on_delete=models.CASCADE, related_name="server_links"
    )
    server_uid = models.CharField(max_length=36, db_index=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["spectrum", "server"], name="unique_server_spectrum"
            )
        ]

    def __str__(self):
        return f"Spectrum: {self.spectrum_uid} - Server: {self.server_uid}"


class Server(BaseModelWithSlug):
    # foreignkey fields
    owner = models.ForeignKey(
        "core.User", on_delete=models.PROTECT, related_name="owned_servers"
    )
    owner_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    description = models.TextField()
    member_limit = models.BigIntegerField(
        default=1000000, help_text="how many users can join this server?"
    )
    server_data = models.JSONField(default=dict, blank=True)
    channel_data = models.JSONField(default=dict, blank=True)

    # url fields
    icon_url = models.TextField(default="", blank=True)
    banner_url = models.TextField(default="", blank=True)

    # reverse relation fields
    # call "spectra" to fetch all the spectrums of a server instance

    def save(self, *args, **kwargs):
        if not self.owner:
            raise ValueError("Owner must always be set!!")
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Server: {self.uid} -Owner: {self.owner_uid}"


class Category(BaseModelWithSlug):
    # foreignkey fields
    server = models.ForeignKey(
        "server.Server",
        on_delete=models.CASCADE,
        related_name="categories",
    )
    server_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    position = models.FloatField(db_index=True)
    is_private = models.BooleanField(
        default=False,
        help_text="is the category private? (only visible to members with access)",
    )

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["server", "name"], name="unique_server_category"
            )
        ]

    def __str__(self):
        return f"Category: {self.name} - Server: {self.server}"


class Channel(BaseModelWithSlug):
    # foreignkey fields
    server = models.ForeignKey(
        "server.Server",
        on_delete=models.CASCADE,
        related_name="channels",
    )
    server_uid = models.CharField(max_length=36, db_index=True, blank=True)

    category = models.ForeignKey(
        "server.Category", on_delete=models.CASCADE, related_name="channels"
    )
    category_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    type = models.CharField(
        max_length=20, choices=ChannelTypes, default=ChannelTypes.TEXT
    )
    member_limit = models.BigIntegerField(
        default=1000000, help_text="how many users can join this channel?"
    )
    position = models.FloatField(db_index=True)
    is_private = models.BooleanField(default=False, help_text="is the channel private?")
    slow_mode = models.IntegerField(
        default=0, help_text="how many seconds should pass between messages?"
    )
    bit_rate = models.IntegerField(
        null=True, blank=True, help_text="Used for voice channels"
    )

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"], name="unique_category_channel"
            )
        ]

    def __str__(self):
        return f"Channel: {self.name} - Server: {self.server}"


class Thread(BaseModelWithSlug):
    # foreignkey fields
    server = models.ForeignKey(
        "server.Server", on_delete=models.CASCADE, related_name="threads"
    )
    server_uid = models.CharField(max_length=36, db_index=True, blank=True)

    category = models.ForeignKey(
        "server.Category", on_delete=models.CASCADE, related_name="threads"
    )
    channel = models.ForeignKey(
        "server.Channel",
        on_delete=models.CASCADE,
        related_name="threads",
    )
    channel_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    position = models.FloatField(db_index=True)
    is_archived = models.BooleanField(default=False)
    auto_archive_duration = models.IntegerField(
        default=30, help_text="stays active for 30 days by default"
    )

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "name"], name="unique_channel_thread"
            )
        ]

    def __str__(self):
        return f"Thread: {self.name} - Channel: {self.channel}"


class Role(BaseModelWithSlug):
    # foreignkey fields
    created_by = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True)
    server = models.ForeignKey(
        "server.Server", on_delete=models.CASCADE, related_name="roles"
    )
    server_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    color = models.CharField(max_length=7, blank=True, default="#FFFFFF")
    position = models.FloatField(db_index=True)

    # url fields
    icon_url = models.TextField(default="", blank=True)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(
                fields=["server", "name"], name="unique_server_role"
            )
        ]

    def __str__(self):
        return f"Role: {self.name} - Server: {self.server}"


class RolePermission(BaseModelWithUID):
    # foreignkey fields
    role = models.ForeignKey(
        "server.Role", on_delete=models.CASCADE, related_name="role_permissions"
    )
    role_uid = models.CharField(max_length=36, db_index=True, blank=True)
    permission = models.ForeignKey("permission.Permission", on_delete=models.CASCADE)
    permission_uid = models.CharField(max_length=36, db_index=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"], name="unique_role_permission"
            )
        ]

    def __str__(self):
        return f"Role: {self.role.name} - Permission: {self.permission.name}"


# class PermissionOverride(BaseModelWithUID):
#     channel = models.ForeignKey(
#         "server.Channel", on_delete=models.CASCADE, null=True, blank=True
#     )
#     category = models.ForeignKey(
#         "server.Category", on_delete=models.CASCADE, null=True, blank=True
#     )
#     role = models.ForeignKey(
#         "server.Role", on_delete=models.CASCADE, null=True, blank=True
#     )
#     member = models.ForeignKey(
#         "member.Member", on_delete=models.CASCADE, null=True, blank=True
#     )
#     user = models.ForeignKey(
#         "core.User", on_delete=models.CASCADE, null=True, blank=True
#     )
#     allow_permissions = models.JSONField(null=True, blank=True)
#     deny_permissions = models.JSONField(null=True, blank=True)


# class AuditLog(BaseModelWithUID):
#     # foreignkey fields
#     member = models.ForeignKey("member.Member", on_delete=models.CASCADE)
#     member_uid = models.CharField(max_length=36, db_index=True, blank=True)

#     server = models.ForeignKey(
#         "server.Server", on_delete=models.CASCADE, related_name="audit_logs"
#     )
#     server_uid = models.CharField(max_length=36, db_index=True, blank=True)

#     # model fields
#     action = models.CharField(db_index=True)
#     details = models.TextField(blank=True)


class Invite(BaseModelWithUID):
    # foreignkey fields
    server = models.ForeignKey(
        "server.Server", on_delete=models.CASCADE, related_name="invites"
    )
    server_uid = models.CharField(max_length=36, db_index=True, blank=True)
    inviter = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sent_invites",
    )
    inviter_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    code = models.CharField(max_length=32, unique=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    uses = models.IntegerField(default=0)
    max_uses = models.IntegerField(default=0, help_text="0 means unlimited")

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=7)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Invite: {self.code} - Server: {self.server} - Inviter: {self.inviter}"

    @property
    def is_valid(self):
        if self.is_deleted or self.server.is_deleted:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        if self.max_uses and self.uses >= self.max_uses:
            return False
        return True
