import logging

from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save

from projectile.core.models import User
from projectile.server.models import Server
from projectile.member.models import Member

logger = logging.getLogger(__name__)
"""
server_data_example
{
    "uid_1": {
        "is_member": False,
        "joined_at": "2025-06-03T10:30:36.947449+00:00",
        "left_at": "2025-06-03T10:30:36.947449+00:00",
    },
    .....
}
"""


@receiver(post_save, sender=Member)
def update_user_server_data(sender, instance: Member, created: bool, **kwargs) -> None:
    try:
        user: User = instance.user
        data: dict = {
            "is_member": True,
            "joined_at": (
                instance.created_at.isoformat() if instance.created_at else None
            ),
            "left_at": None,
        }
        if created:
            user.server_data[instance.server_uid] = data
        elif instance.is_deleted:
            data["is_member"] = False
            data["left_at"] = now().isoformat()
            user.server_data[instance.server_uid] = data
        else:
            data["is_member"] = True
            data["joined_at"] = now().isoformat()
            user.server_data[instance.server_uid] = data

        user.save(update_fields=["server_data"])
        logger.debug(
            f"Updated server_data for user {user.id} and server {instance.server_uid}: {data}"
        )
    except Exception as e:
        logger.exception(f"Failed to update server_data for Member {instance.pk}: {e}")
