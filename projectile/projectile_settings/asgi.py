import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "projectile.projectile_settings.settings"
)
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


def get_jwt_auth_middleware_stack():
    """
    running imports only after Django is initialized, to prevent AppRegistryNotReady errors.
    JWTAuthMiddleware depends on the model core.USER
    and websocket_urlpatterns depends on ChatConsumer which depends on database models.
    this causes errors if imported before django_asgi_app is initialized.
    """
    from chat.middleware import JWTAuthMiddleware
    from chat.routing import websocket_urlpatterns

    return JWTAuthMiddleware(URLRouter(websocket_urlpatterns))


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(get_jwt_auth_middleware_stack()),
    }
)
