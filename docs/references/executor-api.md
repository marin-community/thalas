# Executor API

The Thalas executor framework provides the infrastructure for running reproducible computational experiments with automatic caching and dependency management.

## Core Components

### Executor Entrypoint
- `thalas.execution.executor_main` - The main entry point for running experiments
- `thalas.execution.ExecutorMainConfig` - Configuration for the executor

### Executor and Steps
- `thalas.execution.Executor` - The main executor class
- `thalas.execution.ExecutorStep` - Base class for defining pipeline steps

### Inputs and Outputs
- `thalas.execution.InputName` - Specifying input dependencies
- `thalas.execution.output_path_of` - Getting output paths from steps
- `thalas.execution.this_output_path` - Reference to current step's output
- `thalas.execution.OutputName` - Named outputs
- `thalas.execution.THIS_OUTPUT_PATH` - Constant for current output path

### Versioning
- `thalas.execution.VersionedValue` - Versioned configuration values
- `thalas.execution.versioned` - Creating versioned values
- `thalas.execution.ensure_versioned` - Ensuring values are versioned
- `thalas.execution.unwrap_versioned_value` - Extracting values from versioned wrappers
- `thalas.execution.get_executor_step` - Getting executor steps

## Usage Example

```python
from dataclasses import dataclass
from thalas.execution import (
    ExecutorStep,
    executor_main,
    output_path_of,
    this_output_path
)

@dataclass(frozen=True)
class MyConfig:
    input_path: str
    output_path: str

def my_function(config: MyConfig):
    # Process data from input_path
    # Write results to output_path
    pass

step = ExecutorStep(
    name="my_step",
    description="Process data",
    fn=my_function,
    config=MyConfig(
        input_path=output_path_of(previous_step),
        output_path=this_output_path()
    )
)

if __name__ == "__main__":
    executor_main(steps=[step])
```

## Ray Integration

The executor framework integrates with Ray for distributed computing:

```python
import ray

@ray.remote
def distributed_function(config):
    # This will run on a Ray cluster
    pass

distributed_step = ExecutorStep(
    name="distributed_step",
    fn=distributed_function,
    config=config,
    pip_dependency_groups=["my_dependencies"]
)
```

For more details, see the [Executor Tutorial](../tutorials/executor-101.md) and [Executor Explanation](../explanations/executor.md).