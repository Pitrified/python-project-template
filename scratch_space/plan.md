# Plan

## params/config full setup

add in sample params the correct config/params splitting with env type
config should be a property (cached if possible)
with optional config(for=SomeStrEnum.value) to pick a different value of config if it can hold more than one

## python 3.14

migrate this template

## zensical

mkdocs substituted with zensical

## paths

never use weird `parent.parent` paths, we have custom `ProjectPaths` ready for this
update copilot instruction to explain paths pattern

## default settings in .vscode

add some more default settings in the local vscode setup
eg extensions, linting, colors
