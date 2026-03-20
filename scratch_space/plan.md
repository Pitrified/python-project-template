# Plan

## Do not copy all files

filter some files from scratch space
do not copy meta folder
change this plan file

## Change internal copilot instruction

in renamed project prepare a skeleton -> first task in new project update internal copilot instruction
`scratch_space/vibes/01-post-rename-cleanup.md` is the file with the update plan

## Add check on names

project name cannot have `-` in it

## params/config full setup

add in sample params the correct config/params splitting with env type
config should be a property (cached if possible)
with optional config(for=SomeStrEnum.value) to pick a different value of config if it can hold more than one

## git flow in readme post create

if you have a new project you have an empty git repo, need to setup the remote

## python 3.14

migrate this template

## zensical

mkdocs substituted with zensical

## paths

never use weird `parent.parent` paths, we have custom `ProjectPaths` ready for this
update copilot instruction to explain paths pattern

## pytest async

pytest async always as dep
