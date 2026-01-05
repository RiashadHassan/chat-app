from django.db import models
from django.db.models import Q, Manager


class UserConnectionManager(models.Manager):
    def get_active_qs(self):
        """Return all non-deleted connections"""
        return self.get_queryset().filter(is_deleted=False)

    def get_user_connections(self, user_uid):
        """Return all non-deleted connections for a given user."""
        return self.get_active_qs().filter(
            Q(left_user_uid=user_uid) | Q(right_user_uid=user_uid),
        )

    def get_specific_user_connection(self, user_uid_1, user_uid_2):
        """Return the unique connection between two users, if it exists."""
        left_uid, right_uid = sorted([user_uid_1, user_uid_2])
        return self.get_active_qs().filter(
            left_user_uid=left_uid, right_user_uid=right_uid
        )
