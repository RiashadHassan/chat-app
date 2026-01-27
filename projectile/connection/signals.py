from django.utils import timezone
from django.dispatch import receiver
from django.db import transaction

from django.db.models.signals import post_save


from connection.choices import ConnectionRequestStatus
from connection.models import ConnectionRequest, UserConnection


@receiver(post_save, sender=ConnectionRequest)
def ensure_connection_exists(
    sender, instance: ConnectionRequest, created: bool, **kwargs
):
    """
    When a ConnectionRequest is ACCEPTED, get_or_create an UserConnection instance
    update the ConnectionRequest (con_req.created_connection=user_con)
    empty returns if created or status!=ACCEPTED
    empty return if created_connection_id exists to avoid recursive signals on save

    """
    if created:
        return
    if instance.status != ConnectionRequestStatus.ACCEPTED:
        return
    if instance.created_connection_id:
        return  # prevents recursive re-entry on the save() used below

    # only trigger when an existing req is ACCEPTED
    with transaction.atomic():
        connection, created = UserConnection.objects.get_or_create(
            left_user=instance.sender,
            right_user=instance.receiver,
        )
        instance.created_connection = connection
        instance.save(update_fields=["created_connection"])

        if not created:
            connection.is_deleted = False
            connection.last_accepted_date = timezone.now()
            connection.save(update_fields=["is_deleted", "last_accepted_date"])


# @receiver(post_save, sender=UserConnection)
# def delete_connection_req_on_user_connection_soft_delete(
#     sender, instance: UserConnection, created: bool, **kwargs
# ):
#     if created:
#         return

#     if not instance.is_deleted:
#         return

#     ConnectionRequest.objects.filter(created_connection=instance).delete()
