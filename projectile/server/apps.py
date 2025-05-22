from django.apps import AppConfig


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projectile.server'

    def ready(self):
        from projectile.server import signals
        import projectile.elastic.documents.server
