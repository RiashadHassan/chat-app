ASGI_APPLICATION = "projectile_settings.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # for when we use venv instead of docker :)
            # "hosts": [("127.0.0.1", 6379)],

            # because redis is accessible by its service name inside docker
            "hosts": [("redis", 6379)],
        },
    },
}
