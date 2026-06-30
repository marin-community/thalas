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

from thalas.execution.context import ExecutorContext, current_executor_context, executor_context
from thalas.execution.executor import (
    Executor,
    ExecutorInfo,
    ExecutorMainConfig,
    compute_output_path,
    executor_main,
    materialize,
    resolve_executor_step,
    resolve_local_placeholders,
    unwrap_versioned_value,
    walk_config,
)
from thalas.execution.types import (
    THIS_OUTPUT_PATH,
    ExecutorStep,
    InputName,
    OutputName,
    VersionedValue,
    ensure_versioned,
    get_executor_step,
    output_path_of,
    this_output_path,
    versioned,
)
from thalas.execution.executor_step_status import (
    STATUS_DEP_FAILED,
    STATUS_FAILED,
    STATUS_RUNNING,
    STATUS_SUCCESS,
)
