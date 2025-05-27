import random
from datetime import datetime, timezone


def generate_invite_code(slug: str) -> str:
    now = datetime.now(timezone.utc)
    charset = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    prefix = "".join(word[0].upper() for word in slug.split("-"))
    date_code = f"{now:%y%m%d%H%M%S}"
    remainder = 32 - (len(prefix) + len(date_code))
    suffix = "".join(random.choices(charset, k=remainder))

    return f"{prefix}{date_code}{suffix}"
