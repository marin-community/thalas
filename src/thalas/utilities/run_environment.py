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

import importlib
import logging
import os
from copy import deepcopy

from fray.cluster import GpuConfig, ResourceConfig, TpuConfig

logger = logging.getLogger(__name__)

VLLM_TARGET_DEVICE_ENV = "VLLM_TARGET_DEVICE"
VLLM_TPU_TARGET_DEVICE = "tpu"


def _cli_helpers_module():
    return importlib.import_module("levanter.infra.cli_helpers")


def add_run_env_variables(env: dict[str, str]) -> dict[str, str]:
    """Add run metadata and required eval env vars to a process environment."""
    env = deepcopy(env)

    git_commit = env.get("GIT_COMMIT") or os.environ.get("GIT_COMMIT")
    if not git_commit:
        try:
            git_commit = _cli_helpers_module().get_git_commit()
        except Exception:
            git_commit = None

    if git_commit:
        env["GIT_COMMIT"] = git_commit
    else:
        logger.warning("Failed to find or infer git commit for logging.")

    if "HF_DATASETS_TRUST_REMOTE_CODE" not in env:
        env["HF_DATASETS_TRUST_REMOTE_CODE"] = "1"
    if "HF_ALLOW_CODE_EVAL" not in env:
        env["HF_ALLOW_CODE_EVAL"] = "1"
    if "TOKENIZERS_PARALLELISM" not in env:
        env["TOKENIZERS_PARALLELISM"] = "false"
    if "TPU_MIN_LOG_LEVEL" not in env:
        env["TPU_MIN_LOG_LEVEL"] = "2"
    if "TPU_STDERR_LOG_LEVEL" not in env:
        env["TPU_STDERR_LOG_LEVEL"] = "2"
    if "JAX_COMPILATION_CACHE_DIR" not in env and (val := os.environ.get("JAX_COMPILATION_CACHE_DIR")):
        env["JAX_COMPILATION_CACHE_DIR"] = val

    return env


def extras_for_resources(resources: ResourceConfig) -> list[str]:
    """Return the uv extras for a resource device config."""
    device = resources.device
    if isinstance(device, TpuConfig):
        return ["tpu"]
    if isinstance(device, GpuConfig):
        return ["gpu"]
    return []


def dependency_groups_for_resources(
    resources: ResourceConfig,
    dependency_groups: list[str] | None,
) -> list[str]:
    """Return explicit dependency groups, or infer accelerator extras from resources."""
    if dependency_groups is not None:
        return dependency_groups
    return extras_for_resources(resources)


def env_vars_for_dependency_groups(
    resources: ResourceConfig,
    dependency_groups: list[str],
    env_vars: dict[str, str] | None,
) -> dict[str, str]:
    """Return environment variables required by the selected dependency groups."""
    env = dict(env_vars or {})
    if "vllm" in dependency_groups and isinstance(resources.device, TpuConfig):
        # vLLM source installs choose CUDA by default unless the TPU target is explicit.
        env.setdefault(VLLM_TARGET_DEVICE_ENV, VLLM_TPU_TARGET_DEVICE)
    return env
