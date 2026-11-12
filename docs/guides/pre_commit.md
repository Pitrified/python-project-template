# Pre commit

## Tool versions

ruff, pyright, nbstripout and detect-secrets are each installed twice:
once by uv into the project environment, from `uv.lock`,
and once by pre-commit into its own environment, from the hook's `rev` in `.pre-commit-config.yaml`.
Nothing ties the two together.
When they differ, `uv run ruff check` and the commit hook judge the same file by different rules:
a file passes one and fails the other, or the formatter rewrites what the other just wrote.

The common way to get there is a range in `pyproject.toml`, such as `ruff>=0.9.6`.
The hook stays at its `rev` while every `uv lock --upgrade` moves the environment to the newest release,
so the two drift apart a little more with each lock update, and a new project made from this template starts drifted.

### The rule

A tool that both a hook and `pyproject.toml` name is pinned exactly in `pyproject.toml`, to the hook's `rev`:

```toml
# Exact, and the same as rev in .pre-commit-config.yaml; bump both together.
"ruff==0.15.6",
```

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Same version as the ruff pin in pyproject.toml; bump both together.
  rev: v0.15.6
```

The `v` prefix belongs to the hook repository's tag names: ruff, pyright and detect-secrets have one, nbstripout does not.

### The check

`scripts/check_tool_pins.py` compares each hook's `rev` with the version in `uv.lock` and fails on a difference,
naming the tool, both versions, and what to change.
It runs as the `tool-pins` hook whenever `.pre-commit-config.yaml`, `uv.lock` or `pyproject.toml` is committed,
and by hand from the repository root:

```bash
python3 scripts/check_tool_pins.py
```

It needs only the standard library, so it runs before `uv sync`.
A hooked tool is checked only if it is listed in the script's `HOOK_PACKAGES` and present in `uv.lock`.

### Moving a tool to a new version

One commit, both files:

1. Find the release: the hook repository's tags, or `uvx ruff@latest --version` (the exact pin keeps `uv lock --upgrade` from showing it).
2. Set the exact pin in `pyproject.toml` and the `rev` in `.pre-commit-config.yaml`.
3. `uv lock`, then `uv sync --all-extras --all-groups`.
4. `uv run pre-commit run --all-files`, and commit whatever a new ruff reformats as part of the same change.
5. `python3 scripts/check_tool_pins.py` passes.

A new ruff often brings new rules under `select = ["ALL"]`. Read what fails before adding ignores.

### Bringing a drifted repository in line

For a repository made from this template before the pins existed:

1. Copy `scripts/check_tool_pins.py` and the `tool-pins` hook from this template.
2. Run the script. It lists every tool whose hook and lock disagree.
3. For each one, choose a version, usually the one in `uv.lock` since that is what the project environment has been running,
   and follow "Moving a tool to a new version" above.

## Other hook versions

For the hooks with no counterpart in `uv.lock` (pre-commit-hooks, and uv-pre-commit, which follows the uv binary rather than a package),
check the repository's releases and take the latest stable tag.
For uv-pre-commit, match the uv you run: `uv self update`, then `uv --version`.
