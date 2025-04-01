# Project name

## Installation

### Setup `uv`

To install the package:

Setup [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

Install the correct [python version](https://docs.astral.sh/uv/guides/install-python/) if needed.

### Install the package

Run the following command:

```bash
uv sync --all-extras --all-groups
```

## Setup

To setup the package, create a `.env` file in `~/cred/project_name/.env` with the following content:

```bash
PROJECT_NAME_SAMPLE_ENV_VAR=sample
```

And for VSCode to recognize the environment file, add the following line to the
workspace [settings file](.vscode/settings.json):

```json
"python.envFile": "/home/pmn/cred/project_name/.env"
```

Note that the path to the `.env` file should be absolute.

## Pre-commit

To install the pre-commit hooks, run the following command:

```bash
pre-commit install
```

Run against all the files:

```bash
pre-commit run --all-files
```

## Testing

To run the tests, use the following command:

```bash
uv run pytest
```

or use the VSCode interface.

## IDEAs

- [x] too
- [ ] many
