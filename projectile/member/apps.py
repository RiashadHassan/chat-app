from django.apps import AppConfig


class MemberConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projectile.member"

    def ready(self):
        from projectile.member import signals
