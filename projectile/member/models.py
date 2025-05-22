from django.db import models

from projectile.base.models import BaseModelWithUID, BaseModelWithSlug


class ServerMember(BaseModelWithUID):
    # foreignkey fields
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, db_index=True, related_name="members"
    )
    user_uid = models.CharField(max_length=36, db_index=True, blank=True)
    server = models.ForeignKey(
        "server.Server", on_delete=models.CASCADE, db_index=True, related_name="servers"
    )
    server_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    accessible_channels = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["server", "user"], name="unique_server_member"
            )
        ]

    def __str__(self):
        return f"User: {self.user} - Server: {self.server.name}"


class MemberRoles(BaseModelWithUID):
    # foreignkey fields
    member = models.ForeignKey(
        "member.ServerMember", on_delete=models.CASCADE, related_name="member_roles"
    )
    member_uid = models.CharField(max_length=36, db_index=True, blank=True)
    role = models.ForeignKey(
        "server.Role", on_delete=models.CASCADE, related_name="role_members"
    )
    role_uid = models.CharField(max_length=36, db_index=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["member", "role"], name="unique_member_role"
            )
        ]

    def __str__(self):
        return f"User: {self.member} - Server: {self.role.name}"
