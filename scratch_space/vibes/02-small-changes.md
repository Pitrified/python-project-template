# tune the template

## Do not copy all files

### Overview

filter some files from scratch space
do not copy meta folder
analyze this repo and compile a list of files that we want to skip, include a section of `maybe` files to be reviewed before implementing this change

### Plan

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

## Add check on names

### Overview

project name cannot have `-` in it when running the rename command
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

## git flow in readme post create

### Overview

if you have a new project you have an empty git repo, need to setup the remote

### Plan
