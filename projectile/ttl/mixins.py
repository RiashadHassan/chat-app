from datetime import timedelta
from typing import ClassVar


class TTLModelMixin:
    """
    Declarative opt-in mixin for TTL-enabled models
    """

    TTL_FIELD: ClassVar[str]
    TTL_DURATION: ClassVar[timedelta]

    @classmethod
    def ttl_enabled(cls) -> bool:
        return bool(getattr(cls, "TTL_DURATION", None))
