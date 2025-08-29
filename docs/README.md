# Thalas Documentation

Thalas is the executor framework that was factored out from the [Marin](https://github.com/marin-community/marin) project. It provides infrastructure for running reproducible computational experiments with automatic caching and dependency management.

## Documentation Structure

- **[Tutorials](tutorials/)**: Step-by-step guides to get started with Thalas
  - [Executor 101](tutorials/executor-101.md): Creating your first experiment

- **[Explanations](explanations/)**: In-depth explanations of how Thalas works
  - [Executor Framework](explanations/executor.md): How the executor manages experiments

- **[References](references/)**: API documentation and technical references
  - [Executor API](references/executor-api.md): Complete API reference

## Quick Start

```python
from thalas.execution import ExecutorStep, executor_main, output_path_of, this_output_path

# Define your steps and run experiments
```

For more information, see the [Executor 101 Tutorial](tutorials/executor-101.md).