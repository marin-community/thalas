import json
import logging
from datetime import timedelta
from pathlib import Path

logger = logging.getLogger("ray")


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return {"days": obj.days, "seconds": obj.seconds, "microseconds": obj.microseconds}
        if isinstance(obj, Path):
            return str(obj)
        # Detect any array adhering to the Python Array API Standard;
        # see https://github.com/data-apis/array-api/issues/150
        if hasattr(obj, "__array_namespace__"):
            return str(obj)
        try:
            return super().default(obj)
        except TypeError:
            logger.warning(f"Could not serialize object of type {type(obj)}: {obj}")
            return str(obj)
