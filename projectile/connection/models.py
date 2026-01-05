from django.db import models

from base.models import BaseModelWithUID
from core.models import User
from connection.choices import ConnectionRequestStatus
from connection.managers import UserConnectionManager


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
    # user with the min() uid is always the left_user
    left_user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="connections_left"
    )
    left_user_uid = models.CharField(max_length=36, db_index=True, blank=True)
    # user with the max() uid is always the left_user
    right_user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="connections_right"
    )
    right_user_uid = models.CharField(max_length=36, db_index=True, blank=True)

    # model fields
    last_accepted_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Most recent accept date if connection was soft deleted previously",
    )

    # custom manager for reusable query methods
    objects = UserConnectionManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["left_user", "right_user"],
                name="unique_connection_pair",
            )
            # if save() works properly, no need for a reverse uniqueness check
        ]

    def save(self, *args, **kwargs):
        # cannonical ordering ONLY on creation
        # NEVER change the order of the users after creation
        if not self.pk and self.left_user and self.right_user:
            left_user, right_user = self.get_ordered_users(
                self.left_user, self.right_user
            )
            self.left_user = left_user
            self.right_user = right_user
        super().save(*args, **kwargs)

    @staticmethod
    def get_ordered_users(user_1: User, user_2: User) -> tuple[User, User]:
        """
        returns a tuple of users in ascending order based on their uids
        """
        if user_1.uid < user_2.uid:
            return (user_1, user_2)
        return (user_2, user_1)


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
