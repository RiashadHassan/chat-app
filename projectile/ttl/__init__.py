from __future__ import annotations

import logging
from typing import Final

# centralized Logger for TTL tasks, don't change it at run-time
TTL_LOGGER: Final[logging.Logger] = logging.getLogger("ttl")
