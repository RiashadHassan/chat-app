from django.dispatch import receiver
from django.db.models.signals import post_save

from core.models import User
from server.models import Server
from member.models import Member


@receiver(post_save, sender=Server)
def server_creation_signal(sender, instance, created, **kwargs):
    if created:
        user = instance.owner
        Member.objects.create(user=user, server=instance)
