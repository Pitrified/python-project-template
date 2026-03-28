# tune the template

## Do not copy all files

### Overview

filter some files from scratch space
do not copy meta folder
analyze this repo and compile a list of files that we want to skip, include a section of `maybe` files to be reviewed before implementing this change

### Analysis

Current `skip_fols` (directories) in `copy_files()`:
```
__pycache__, .pytest_cache, .ruff_cache, .git, .venv, site
```
`meta` is commented out.

Current `skip_portions` (individual files):
```
README.md, poetry.lock, uv.lock, meta/rename_project.py, pyproject.toml
```

`meta/README.md` and `final_resources/README.md` / `final_resources/pyproject.toml`
are handled via `special_portions`, so the meta folder content is partially managed
already. What leaks through: `meta/__init__.py`.

#### Files / folders to SKIP (definite)

| Path | Reason |
|---|---|
| `meta/__init__.py` | Package stub only needed inside the template repo itself | --> make sure that `meta` folder does not appear at all in the new project
| `scratch_space/plan.md` | Internal template planning notes |
| `scratch_space/vibes/` | All vibe/planning docs are template-internal |
| `final_resources/` | Already consumed via `special_portions`; the dir itself should not appear |
| `nokeys.env` | Shows template-specific env var names; the cred file is already created | --> KEEP but plan to update (see change #2)
| `.github/agents/` | Agent definitions reference template internals; should be rebuilt per project | --> KEEP but plan to update (see change #2)

#### Files / folders that are MAYBE

| Path | Reason to keep | Reason to skip |
|---|---|---|
| `scratch_space/feature_sample/` | Shows how to add a feature end-to-end | Low signal once renamed | --> KEEP, will be renamed correctly and is a useful starting point for a notebook
| `scratch_space/project_name_sample/` | Shows canonical usage pattern | May confuse with old name artefacts | --> KEEP, will be renamed correctly and is a useful reference for the config/params pattern
| `scratch_space/webapp_scaffold/` | Useful if the user keeps the webapp | Noise if they strip it | --> SKIP, this was old webapp development scratch and is not polished or meant as a reference
| `scratch_space/mkdocs_integration/` | Useful if the user keeps MkDocs | Noise if they strip it | --> SKIP, this was old MkDocs experimentation and is not polished or meant as a reference
| `.github/copilot-instructions.md` | Copy but plan to update (see change #2) | Keep, it gets updated |

### Plan

1. Add `meta/__init__.py`, `scratch_space/plan.md`, `nokeys.env` to `skip_portions`.
2. Add `final_resources` and `.github/agents` to `skip_fols`.
3. Decide on the "maybe" list above (review before implementing).
4. Add `scratch_space/vibes` to `skip_fols` EXCEPT for
   `scratch_space/vibes/01-post-rename-cleanup.md`, which becomes a `special_portion`
   mapping to `FIRST_TASKS.md` at the new project root (see change #2).
   - Implement by removing `vibes` from `skip_fols` and instead adding every other file
     under `vibes/` to `skip_portions`, OR by restructuring so only
     `01-post-rename-cleanup.md` lives outside `vibes/` before copying.

## Prepare post rename first task instruction

### Overview

`scratch_space/vibes/01-post-rename-cleanup.md` is the file with the update plan
prepare that file so that when it gets renamed in the new project it will have the correct instruction for copilot to follow
eg
* Change internal copilot instruction `new_project/.github/copilot-instructions.md`
* review docs
* clean up unnecessary files in the copied project (webapp, dependencies) -- ask the user if they want to keep them in the renamed project
* ...

### Plan

1. Create `scratch_space/vibes/01-post-rename-cleanup.md` in the template repo. It does
   not exist yet. Write it as a ready-to-use Copilot prompt, not a planning doc.

2. Register it in `copy_files()` as a `special_portion`:
   ```python
   "scratch_space/vibes/01-post-rename-cleanup.md": "FIRST_TASKS.md",
   ```
   This places it at the new project root as `FIRST_TASKS.md`, highly visible.
   UPDATE no just leave it in vibes and add it to skip_fols except for that file,
   mention it in the `meta/README.md` that it should be consulted as the first task.

3. Content to include in `01-post-rename-cleanup.md` (the instructions Copilot should
   follow in the freshly renamed project):
   - **Update `.github/copilot-instructions.md`** - swap out all `project_name` /
     `python-project-template` references for the real project name and purpose.
   - **Review `docs/`** - update `index.md`, `getting-started.md`, and
     `contributing.md` to reflect the new project's purpose.
   - **Webapp** - ask the user: "Do you want to keep the FastAPI webapp?" If no,
     remove `src/<pkg>/webapp/`, `src/<pkg>/config/webapp/`, related
     `pyproject.toml` extras, middleware, and update `README.md`.
   - **MkDocs** - ask the user: "Do you want to keep MkDocs docs?" If no, remove
     `mkdocs.yml`, `docs/`, and the `mkdocs` dependency.
   - **Google OAuth / rate limiting** - ask if these webapp features are needed.
   - **Haystack / AI layer** - ask if the AI/LLM dependencies are needed.
   - **Clean scratch_space** - look for stale notebooks/vibes/other files that are not relevant to the new project and remove them.
   - **Update `README.md`** - replace the template boilerplate with a real description.
   - **Run verification** - `uv run pytest && uv run ruff check . && uv run pyright`.
   - **Setup pre-commit hooks** - run the necessary commands to set up pre-commit hooks for linting and testing on commit.

4. The name_map will translate `project_name`, `ProjectName`, etc. inside the file,
   so any references to the package name will be correct automatically.

## Add check on names

### Overview

project name cannot have `-` in it when running the rename command

### Plan

1. Add a name validation step **before** `build_name_map()` (in `Rename.__init__()` or
   at the top of `check_inputs()`). The rule: `project_name` must be lowercase
   snake_case only - letters, digits, and underscores; no hyphens, spaces, or uppercase.

   ```python
   import re

   VALID_NAME = re.compile(r'^[a-z][a-z0-9_]*$')

   if not VALID_NAME.match(self.project_name):
       rprint("[red]Error: project_name must be snake_case (e.g. my_new_project).[/red]")
       raise typer.Exit(code=1)
   ```

2. Surface a clear error message explaining what is wrong and showing a valid example.

## git flow in readme post create

### Overview

if you have a new project you have an empty git repo, need to setup the remote

integrate the `meta/README.md` with the classic git pattern

```bash
git init
git add ...
git commit -m "bootstrap project"
git branch -M main
git remote add origin https://github.com/<user>/<project>.git
git remote add origin git@github.com:<user>/<project>.git
git push -u origin main
```

### Plan

`meta/README.md` becomes `README_POST_CREATE.md` in the new project via `special_portions`.
The name_map substitutes `python-project-template` → repo_name and `Pitrified`/`pitrified`
→ github_username, so git URLs will be correct if `--github-username` is provided.

1. Add a **"First-time git setup"** section to `meta/README.md` with the following
   template block (name substitutions happen automatically):

   ```bash
   # initialise git and push to GitHub
   git init
   git add .
   git commit -m "bootstrap project"
   git branch -M main
   git remote add origin https://github.com/Pitrified/python-project-template.git
   # or with SSH:
   # git remote add origin git@github.com:Pitrified/python-project-template.git
   git push -u origin main
   ```

2. Place this section **early** in `meta/README.md`, right after the project title /
   brief description, so it is the first thing a developer sees in
   `README_POST_CREATE.md`.

3. Add a note: "If you did not supply `--github-username` when running
   `rename-project`, replace `Pitrified` with your actual GitHub username."

4. Ensure `FIRST_TASKS.md` (from change #2) cross-references `README_POST_CREATE.md`
   so developers know both files exist and which to consult first.
