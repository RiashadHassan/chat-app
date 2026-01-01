from django.db import models

from base.models import BaseModelWithUID
from connection.choices import ConnectionRequestStatus


class ConnectionRequest(BaseModelWithUID):
    # foreignkey fields
    sender = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="sent_requests"
    )
    sender_uid = models.CharField(max_length=36, db_index=True, blank=True)
    receiver = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="received_requests"
    )
    receiver_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    status = models.CharField(
        choices=ConnectionRequestStatus,
        default=ConnectionRequestStatus.PENDING,
        db_index=True,
    )
    rejected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sender_uid", "created_at"]),
            models.Index(fields=["receiver_uid", "created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "receiver"],
                name="unique_friend_request_pair",
            )
        ]


class UserConnection(BaseModelWithUID):
    # foreignkey fields
    # sender of the request is always the left_user
    left_user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="connections_left"
    )
    left_user_uid = models.CharField(max_length=36, db_index=True, blank=True)
    # receiver of the request is always the right_user
    right_user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="connections_right"
    )
    right_user_uid = models.CharField(max_length=36, db_index=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["left_user", "right_user"],
                name="unique_connection_pair",
            )
        ]


class ConnectionBlock(BaseModelWithUID):
    # foreignkey fields
    blocker = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="blocks_created"
    )
    blocker_uid = models.CharField(max_length=36, db_index=True, blank=True)

    blocked = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="blocks_received"
    )
    blocked_uid = models.CharField(max_length=36, db_index=True, blank=True)

    unblocked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["blocker", "blocked"],
                name="unique_block_pair",
            )
        ]
