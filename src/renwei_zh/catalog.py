from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any, cast


@lru_cache(maxsize=1)
def load_catalog() -> dict[str, Any]:
    """Load the bundled pattern catalog."""
    data_file = resources.files("renwei_zh.data").joinpath("patterns.v1.json")
    return cast("dict[str, Any]", json.loads(data_file.read_text(encoding="utf-8")))
