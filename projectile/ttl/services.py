from typing import List, Type

from django.db.models import Model

from projectile.ttl.dto import TTLModelInfo
from projectile.ttl.discovery import TTLModelDiscovery


class TTLIntrospectionService:
    def __init__(self, discovery: TTLModelDiscovery):
        self._discovery = discovery

    def list_ttl_models(self) -> List[TTLModelInfo]:
        results: List[TTLModelInfo] = []

        for model in self._discovery.get_ttl_models():
            results.append(
                TTLModelInfo(
                    app_label=model._meta.app_label,
                    model_name=model._meta.model_name,
                    ttl_field=model.TTL_FIELD,
                    ttl_days=model.TTL_DURATION.days,
                )
            )

        return results
