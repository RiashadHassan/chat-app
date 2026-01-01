from django.dispatch import receiver
from django.db import transaction

from django.db.models.signals import post_save, post_delete


from connection.choices import ConnectionRequestStatus
from connection.models import ConnectionRequest, UserConnection


@receiver(post_save, sender=ConnectionRequest)
def create_user_connection_on_request_accept(
    sender, instance: ConnectionRequest, created: bool, **kwargs
):
    if not created and instance.status == ConnectionRequestStatus.ACCEPTED:
        with transaction.atomic():    
            # request sender is always the left_user, receiver is always the right_user
            UserConnection.objects.create(
                left_user=instance.sender,
                right_user=instance.receiver,
            )


# @receiver(post_delete, sender=UserConnection)
# def delete_connection_request_on_user_connection_delete(
#     sender, instance: UserConnection, **kwargs
# ):
#     ConnectionRequest.objects.filter(
#         sender=instance.left_user,
#         receiver=instance.right_user,
#         status=ConnectionRequestStatus.ACCEPTED,
#     ).delete()
#     ConnectionRequest.objects.filter(
#         sender=instance.right_user,
#         receiver=instance.left_user,
#         status=ConnectionRequestStatus.ACCEPTED,
#     ).delete()
