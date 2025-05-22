from django.dispatch import receiver
from django.db.models.signals import post_save

from projectile.core.models import User
from projectile.server.models import Server
from projectile.member.models import Member


@receiver(post_save, sender=Server)
def server_creation_signal(sender, instance, created, **kwargs):
    if created:
        user = instance.owner
        Member.objects.create(user=user, server=instance)
