import dj_database_url

# DATABASE_ROUTERS = ["projectile.projectile_settings.db_router.DatabaseRouter"]

DATABASES = {
    "default": dj_database_url.config(env="DATABASE_URL"),
    # "replica": dj_database_url.config(env="REPLICA_DATABASE_URL", conn_max_age=600),
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://elasticsearch:9200'  # use service name from docker-compose
    },
}
