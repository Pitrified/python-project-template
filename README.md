# Python project template

Set up a new Python project.

Follow the instructions in the [meta README](meta/README.md) to set up a new project.

Happy coding!

## IDEAs

Fancier automation with github actions.
* https://github.com/rochacbruno/python-project-template

Support codecov.

Support documentation with sphinx or mkdocs.

## TODOs

### Write a script to initialize the project

- [x] Copy the `project_name` folder to the new project name.
- [x] Replace all instances of `project_name` with the new project name.
      With proper capitalization.
- [ ] Remove dependencies from the `pyproject.toml` file.
- [ ] Automagically generate the optional dependencies list,
      by parsing the `pyproject.toml` file.
      The dependencies are the same as the ones in the `pyproject.toml` file,
      but by running `poetry add` again the versions are updated.
- [ ] Refactor rename_project.py to be a class.