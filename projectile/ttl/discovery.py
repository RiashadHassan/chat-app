from typing import Iterable, Type

from django.apps import apps
from django.db.models import Model

from projectile.ttl import TTL_LOGGER
from projectile.ttl.mixins import TTLModelMixin


class TTLModelDiscovery:
    """
    Responsible for discovering TTL-enabled models
    as in Django models that inherit from the TTLModelMixin
    """

    def get_ttl_models(self) -> Iterable[Type[Model]]:
        for model in apps.get_models():
            if self._is_ttl_model(model=model):
                yield model

    def _is_ttl_model(self, model) -> bool:
        return issubclass(model, TTLModelMixin) and model.ttl_enabled()
