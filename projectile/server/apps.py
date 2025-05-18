from django.apps import AppConfig


class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projectile.server'

    def ready(self):
        import projectile.elastic.documents.server
