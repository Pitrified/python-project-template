"""Script to rename a project.

1. Input the new project and repo names.
1. Copy the files to the new project name.
1. Update the contents of the files.
1. Create a credentials file.
"""

from pathlib import Path
from pprint import pprint as pp
import shutil
from typing import Any, Generator


def input_new_name() -> str:
    """Input the new project name."""
    # new_name = input("Enter the new project name: ")
    new_name = "sample_project"
    return new_name


def input_repo_name() -> str:
    """Input the new repo name."""
    # repo_name = input("Enter the new repo name: ")
    repo_name = "repo_sample_project"
    return repo_name


def build_name_map(new_name: str, repo_name: str) -> dict[str, str]:
    """Build the capitalized name."""
    pieces = new_name.split("_")
    kebab_case = "-".join(pieces)
    camel_case = "".join([p.capitalize() for p in pieces])
    pretty = " ".join(pieces).capitalize()
    return {
        "project_name": new_name,
        "PROJECT_NAME": new_name.upper(),
        "project-name": kebab_case,
        "ProjectName": camel_case,
        "Project name": pretty,
        "python_project_template": repo_name,
    }


def replace_in_str(s: str, name_map: dict[str, str]) -> str:
    """Replace all instances of project_name (and variations) in a string."""
    for old, new in name_map.items():
        s = s.replace(old, new)
    return s


def rglobber(fol: Path, skip_fols: list[str]) -> Generator[Path, Any, None]:
    """Recursively glob files, skipping directories."""
    for item in sorted(fol.iterdir()):
        if item.is_dir() and item.name in skip_fols:
            continue
        if item.is_dir():
            yield from rglobber(item, skip_fols)
        else:
            yield item


def copy_files(name_map: dict[str, str]) -> Path:
    """Copy files to the new project name."""
    old_root_fol = Path(__file__).parents[1].resolve()
    print(f"{old_root_fol=}")

    new_root_fol = old_root_fol.parent / name_map["python_project_template"]
    print(f"{new_root_fol=}")

    # skip these directories
    skip_fols = [
        "__pycache__",
        ".pytest_cache",
        ".git",
        # "meta",
    ]
    # skip these files
    skip_portions = [
        "README.md",
        "poetry.lock",
        "rename_project.py",
    ]
    # special cases to rename
    special_portions = {
        "README_FINAL.md": "README.md",
        "meta/README.md": "README_POST_CREATE.md",
    }
    for old_fp in rglobber(old_root_fol, skip_fols):
        # get the portion of the source path relative to the root
        old_relative_portion = old_fp.relative_to(old_root_fol)

        if str(old_relative_portion) in skip_portions:
            print(f"Skipping {old_fp}")
            continue

        if str(old_relative_portion) in special_portions:
            new_relative_portion = Path(special_portions[str(old_relative_portion)])
        else:
            # change the project name in the relative portion
            new_relative_portion = Path(
                replace_in_str(str(old_relative_portion), name_map)
            )
        # print(f"{old_relative_portion=} {new_relative_portion=}")

        # get the destination path
        new_fp = new_root_fol / new_relative_portion
        print(f".  {old_fp}\n     > {new_fp}")

        # ensure the destination directory exists
        new_fp.parent.mkdir(parents=True, exist_ok=True)
        # copy the file
        shutil.copy(old_fp, new_fp)

        # break

    return new_root_fol


def update_file(fp: Path, name_map: dict[str, str]) -> None:
    """Update the contents of a file."""
    contents = fp.read_text()
    new_contents = replace_in_str(contents, name_map)
    fp.write_text(new_contents)


def update_files(new_root_fol: Path, name_map: dict[str, str]) -> None:
    """Update the contents of the files."""
    for new_fp in rglobber(new_root_fol, []):
        update_file(new_fp, name_map)


def create_cred_file(name_map: dict[str, str]) -> None:
    """Create the credentials file."""
    cred_fp = Path.home() / "cred" / name_map["project_name"] / ".env"
    cred_fp.parent.mkdir(parents=True, exist_ok=True)
    sample_cred = f'{name_map["PROJECT_NAME"]}_SAMPLE_ENV_VAR="sample"'
    cred_fp.write_text(sample_cred)


def main() -> None:
    """Rename a project."""
    new_name = input_new_name()
    repo_name = input_repo_name()
    name_map = build_name_map(new_name, repo_name)
    pp(name_map, sort_dicts=False)

    new_root_fol = copy_files(name_map)
    update_files(new_root_fol, name_map)

    create_cred_file(name_map)


if __name__ == "__main__":
    main()
