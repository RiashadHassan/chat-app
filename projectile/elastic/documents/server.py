from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from projectile.server.models import Server


@registry.register_document
class ServerDocument(Document):
    uid = fields.KeywordField(attr="uid")
    slug = fields.KeywordField(attr="slug")
    name = fields.KeywordField(attr="name")
    owner_uid = fields.TextField(attr="owner.uid")
    owner_username = fields.TextField(attr="owner.username")

    class Index:
        name = "server.server"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Server

        fields = [
            "created_at",
            "updated_at",
            "description",
            "is_deleted",
        ]

    # def get_queryset(self):
    #     return super().get_queryset().filter(is_deleted=False).select_related("owner")
