# Thalas

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install the package
4. Set up pre-commit hooks

```bash
git clone https://github.com/Open-Athena/thalas.git
cd thalas
uv venv --python 3.11
source .venv/bin/activate
uv pip install -e .[dev]
pre-commit install
```
