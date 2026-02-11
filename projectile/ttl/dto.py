from dataclasses import dataclass


@dataclass(frozen=True)
class TTLModelInfo:
    app_label: str
    model_name: str
    ttl_field: str
    ttl_days: int
