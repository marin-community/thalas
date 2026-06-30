# Copyright 2025-2026 The Thalas Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import dataclasses
import json
import logging
from datetime import timedelta
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class CustomJsonEncoder(json.JSONEncoder):
    """JSON encoder for executor configs.

    Handles the value types that show up in step configs: timedeltas, paths,
    enums, numeric dtype objects (numpy/jax/torch), and dataclasses. Dtype
    handling is duck-typed so we do not need a hard dependency on an array
    library just to serialize a config.
    """

    def default(self, o):
        if isinstance(o, timedelta):
            return {"days": o.days, "seconds": o.seconds, "microseconds": o.microseconds}
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, Enum):
            return o.value
        if self._is_dtype(o):
            return str(o)
        if dataclasses.is_dataclass(o) and not isinstance(o, type):
            return dataclasses.asdict(o)
        try:
            return super().default(o)
        except TypeError:
            logger.warning(f"Could not serialize object of type {type(o)}: {o}")
            return str(o)

    @staticmethod
    def _is_dtype(o):
        """Whether ``o`` is a scalar dtype object (numpy/jax/torch), not an array.

        Dtype objects expose ``name`` and ``itemsize`` but have no ``shape``;
        that distinguishes them from array instances.
        """
        return hasattr(o, "name") and hasattr(o, "itemsize") and not hasattr(o, "shape")
