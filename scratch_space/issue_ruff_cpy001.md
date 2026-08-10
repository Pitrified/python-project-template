# Issue draft: ruff 0.16 breaks lint in every new project (CPY001)

Draft for a GitHub issue on `python-project-template`. Found while rebooting `abyss` onto the
template, 2026-08-10.

---

## Title

`select = ["ALL"]` + ruff 0.16 fails lint on a fresh project: CPY001 wants a copyright notice

## Body

**Every project generated from the template now fails `ruff check` on the first run**, with one
error per Python file, before a line of project code is written.

### What happens

`ruff.toml` sets `select = ["ALL"]`, and `pyproject.toml` pins only `ruff>=0.9.6`. A new project
resolves the newest ruff, which is 0.16.x today. Ruff 0.16 stabilised `CPY001`
(`missing-copyright-notice`, from flake8-copyright), so `ALL` now includes it, and the fleet uses
no copyright headers anywhere.

Reproduced against this repo:

```console
$ uv run ruff --version          # what the committed lock installs
ruff 0.15.6
$ uv run ruff check .
All checks passed!

$ uvx ruff@0.16.2 check .        # what a fresh `uv sync` resolves
Found 49 errors.
$ uvx ruff@0.16.2 check . --statistics
49  CPY001  missing-copyright-notice
```

CPY001 is the *only* new failure - nothing else in the template trips on 0.16.

The mechanism, for the record:

```console
$ uvx ruff@0.15.6 check . --select CPY001
warning: Selection `CPY001` has no effect because preview is not enabled.
All checks passed!

$ uvx ruff@0.15.6 check . --select CPY001 --preview
Found 49 errors.
```

So the rule was preview-only in 0.15 and is on by default in 0.16. Nothing in the template
changed; the linter did.

### Why it is not visible here

This repo has a committed `uv.lock` pinning ruff 0.15.6, so `make lint` passes. The breakage only
shows up in a project that resolves fresh - which is exactly what `meta/rename_project.py` produces.
`abyss` hit it immediately on its first `uv sync`.

### Suggested fix

Add `CPY001` to the ignore list in `ruff.toml`:

```toml
ignore = [
    "COM812", # Missing trailing comma, conflict with the formatter
    "CPY001", # Missing copyright notice: private repos, no notices anywhere in the fleet
    ...
]
```

`abyss` already carries this line; the fix belongs upstream so the next project does not rediscover
it.

### Second-order problem, worth a decision

`.pre-commit-config.yaml` pins `rev: v0.15.2` for the ruff hook, while `pyproject.toml` says
`ruff>=0.9.6`. The comment above the rev says "uv run ruff --version", i.e. the two are meant to
match - but nothing enforces it, and they are already three patch versions apart here. In a fresh
project the gap becomes a major-ish one: the hook lints with 0.15.2 while the editor and `make lint`
use 0.16.x, so `pre-commit run --all-files` and `make lint` can legitimately disagree.

Options:

1. **Pin ruff in `pyproject.toml`** to the same minor as the hook (`ruff>=0.16,<0.17`), and bump
   both together. Deliberate, one place to change, no drift.
2. **Keep the floor open** and accept that the hook lags, treating `make lint` as authoritative.
   Cheapest, but the disagreement stays.
3. **Drop the pinned rev** in favour of the local ruff (`repo: local` hook running `uv run ruff`).
   Always consistent, but loses pre-commit's isolated environment.

Same question applies to `pyright` and `nbstripout`, which have the same "match the uv version"
comment.

### Related

The general shape of this - `select = ["ALL"]` means every ruff release can add work to every repo
in the fleet - is worth a line in `docs/guides/pre_commit.md`, next to the existing instructions for
keeping hook revisions current.
