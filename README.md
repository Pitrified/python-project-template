# Python project template

Set up a new Python project.

Follow the instructions in the [meta README](meta/README.md) to set up a new project.

Happy coding!

## Documentation

Build and serve the documentation locally:

```bash
# Install docs dependencies
uv sync --group docs

# Start local server with hot reload
uv run mkdocs serve

# Build static site
uv run mkdocs build

# Deploy to GitHub Pages
uv run mkdocs gh-deploy
```

## IDEAs

Fancier automation with github actions (eg):

- https://github.com/rochacbruno/python-project-template

Support codecov.

Automatic dependency updates with [uv-bump](https://github.com/zundertj/uv-bump).

Expose a minimal FastAPI app.

Expose a minimal CLI app with [Typer](https://typer.tiangolo.com/).

Convert the whole thing to a [Copier](https://copier.readthedocs.io/en/stable/) template.

Town crier integration.

Release management with semantic versioning.

Move the entire package in a `template` subfolder.
That is the real package that will be copied and renamed.
Only leave renamer related things here.
Maybe some ruff/precommit configs can be shared.
The internal package can be installed by going in the `template` folder and treating it as a separate folder.

## TODOs

### Write a script to initialize the project (renamer)

- [ ] Remove dependencies from the `pyproject.toml` file.
- [ ] Automagically generate the optional dependencies list,
      by parsing the `pyproject.toml` file.
      The dependencies are the same as the ones in the `pyproject.toml` file,
      but by running `uv add` again the versions are updated.

### pyproject.toml structure

- [x] Split dev dependencies into groups
  - [x] lint
  - [x] test
  - [ ] doc (?? we don't have any doc specific deps yet)
  - [ ] ci (?? we don't have any ci specific deps yet)
- [ ] Add optional dependencies (extra sections)
  - [ ] some optional feature
  - [ ] full (all optional dependencies)

### Detect secret

- [ ] add info on how to keep it updated
- [ ] add info on how to set it up
- [ ] add info on how to handle false positives

### Check that proj name is valid python package name

- [ ] add check in renamer script
  - [ ] check for invalid characters (eg `-`, spaces, etc)
- [ ] add info in readme

### Get names from CLI

- [ ] get project name from CLI arguments
