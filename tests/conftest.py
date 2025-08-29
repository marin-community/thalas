# Copyright 2025 The Marin Authors
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

import os
import sys
from pathlib import Path

import fasteners
import pytest
import ray
from pydantic import BaseModel


class WorkerConfig(BaseModel):
    worker_count: int = 0
    cluster_address: str | None = None


@pytest.fixture(scope="session")
def ray_tpu_cluster(tmp_path_factory, worker_id):
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    config_file = Path(root_tmp_dir) / "ray_cluster_config.json"
    lock_file = Path(root_tmp_dir) / "ray_cluster_config.lock"
    rw_lock = fasteners.InterProcessReaderWriterLock(str(lock_file))

    def _start_cluster():
        print(f"Worker {worker_id} starting Ray cluster...", file=sys.stderr)

        if os.getenv("START_RAY_TPU_CLUSTER") == "true":
            ray.init(
                namespace="marin",
                resources={"TPU": 8, "TPU-v6e-8-head": 1, "head_node": 1},
                num_cpus=120,
                ignore_reinit_error=True,
            )
        elif os.getenv("START_RAY_CPU_CLUSTER") == "true":
            ray.init(namespace="marin", num_cpus=8, resources={"head_node": 1}, ignore_reinit_error=True)
        else:
            ray.init(namespace="marin", num_cpus=8, resources={"head_node": 1}, ignore_reinit_error=True)
        return ray.worker._global_node.address

    def _init_worker():
        with rw_lock.write_lock():
            if not config_file.exists():
                # First worker to acquire lock - initialize cluster
                config = WorkerConfig(cluster_address=_start_cluster(), worker_count=1)
                with open(config_file, "w") as f:
                    f.write(config.model_dump_json())
                return config

            # Config file exists, increment worker count and connect to existing cluster
            with open(config_file, "r") as f:
                content = f.read().strip()
            current_config = WorkerConfig.model_validate_json(content)
            current_config.worker_count += 1

            # Connect to the existing cluster
            ray.init(
                address=current_config.cluster_address,
                resources={"head_node": 1},
                namespace="marin",
                ignore_reinit_error=True,
            )

            print(
                f"Worker {worker_id} connected to cluster at {current_config.cluster_address}, "
                f"worker count {current_config.worker_count}",
                file=sys.stderr,
            )
            with open(config_file, "w") as f:
                f.write(current_config.model_dump_json())

            return current_config

    def _shutdown_worker():
        with rw_lock.write_lock():
            with open(config_file, "r") as f:
                content = f.read().strip()
            current_config = WorkerConfig.model_validate_json(content)
            current_config.worker_count -= 1
            print(
                f"Worker {worker_id} shutting down... worker count {current_config.worker_count}",
                file=sys.stderr,
            )
            if current_config.worker_count == 0:
                # Delete file under lock
                config_file.unlink()
                print("Last worker shutting down Ray cluster...", file=sys.stderr)
                ray.shutdown()
            else:
                with open(config_file, "w") as f:
                    f.write(current_config.model_dump_json())

    config = _init_worker()
    os.environ["RAY_ADDRESS"] = config.cluster_address
    yield
    _shutdown_worker()
