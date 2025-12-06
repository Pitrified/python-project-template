# Python project template

Set up a new Python project.

Follow the instructions in the [meta README](meta/README.md) to set up a new project.

Happy coding!

## IDEAs

Fancier automation with github actions.

- https://github.com/rochacbruno/python-project-template

Support codecov.

Support documentation with sphinx or mkdocs.

Automatic dependency updates with [uv-bump](https://github.com/zundertj/uv-bump).

Expose a minimal FastAPI app.

Expose a minimal CLI app with [Typer](https://typer.tiangolo.com/).

Convert the whole thing to a [Copier](https://copier.readthedocs.io/en/stable/) template.

Town crier integration.

Release management with semantic versioning.

## TODOs

### Write a script to initialize the project

- [ ] Remove dependencies from the `pyproject.toml` file.
- [ ] Automagically generate the optional dependencies list,
      by parsing the `pyproject.toml` file.
      The dependencies are the same as the ones in the `pyproject.toml` file,
      but by running `uv add` again the versions are updated.

### Vibes

- [ ] Add agents to maintain the project.
  - [ ] meta agent to maintain the agents themselves and general instructions
  - [ ] dependency update agent
  - [ ] test agent
  - [ ] documentation agent

### Tests

- [ ] Add tests for new features

### pyproject.toml structure

- [ ] Split dev dependencies into groups
  - [ ] lint
  - [ ] test
  - [ ] doc
  - [ ] ci
- [ ] Add optional dependencies (extra sections)
  - [ ] some optional feature
  - [ ] full (all optional dependencies)

### Detect secret

- [ ] add info on how to keep it updated
- [ ] add info on how to set it up
- [ ] add info on how to handle false positives
