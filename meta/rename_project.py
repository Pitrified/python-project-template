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


def update_file_content(fp: Path, name_map: dict[str, str]) -> None:
    """Update the contents of a file."""
    contents = fp.read_text()
    new_contents = replace_in_str(contents, name_map)
    fp.write_text(new_contents)


class Rename:
    """Class to rename a project."""

    def __init__(self):
        """Initialize the Rename class."""
        self.get_inputs()
        self.build_name_map()
        self.build_roots()
        self.build_cred_fp()

    def get_inputs(self) -> None:
        """Get the new project and repo names."""
        self.new_name = input("Enter the new project name: ")
        # self.new_name = "sample_project"
        repo_prompt = f"Enter the new repo name [{self.new_name}]: "
        self.repo_name = input(repo_prompt) or self.new_name
        # self.repo_name = "repo_sample_project"

    def build_name_map(self) -> None:
        """Build the capitalized name."""
        pieces = self.new_name.split("_")
        kebab_case = "-".join(pieces)
        camel_case = "".join([p.capitalize() for p in pieces])
        pretty = " ".join(pieces).capitalize()
        self.name_map = {
            "project_name": self.new_name,
            "PROJECT_NAME": self.new_name.upper(),
            "project-name": kebab_case,
            "ProjectName": camel_case,
            "Project name": pretty,
            "python_project_template": self.repo_name,
        }
        print("Name map:")
        pp(self.name_map, sort_dicts=False)

    def build_roots(self) -> None:
        """Build the roots of the old and new projects."""
        self.old_root_fol = Path(__file__).parents[1].resolve()
        # print(f"{self.old_root_fol}")

        self.new_root_fol = (
            self.old_root_fol.parent / self.name_map["python_project_template"]
        )
        print(f"Will init the project in {self.new_root_fol}")

    def build_cred_fp(self) -> None:
        """Build the credentials file path."""
        self.cred_fp = Path.home() / "cred" / self.name_map["project_name"] / ".env"

    def check_inputs(self) -> bool:
        """Check that the project name is correct and not already in use."""
        # check that the new project name is correct
        print("Is the above information correct?")
        valid = input("Continue? ([y]/n) ")
        if not (valid == "" or valid.lower() == "y"):
            print("Error: Wrong information.")
            return False
        # check that the new project name is not already in use
        if self.new_root_fol.exists():
            print(f"Error: {self.new_root_fol} already exists.")
            return False
        if self.cred_fp.exists():
            print(f"Error: {self.cred_fp} already exists.")
            return False
        return True

    def copy_files(self) -> None:
        """Copy files to the new project name."""
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
        for old_fp in rglobber(self.old_root_fol, skip_fols):
            # get the portion of the source path relative to the root
            old_relative_portion = old_fp.relative_to(self.old_root_fol)

            # skip certain files
            if str(old_relative_portion) in skip_portions:
                # print(f"Skipping {old_fp}")
                continue

            # change the file name in the relative portion
            if str(old_relative_portion) in special_portions:
                # change the file name in a custom way
                new_relative_portion = Path(special_portions[str(old_relative_portion)])
            else:
                # change the file name in the standard way with the name map
                new_relative_portion = Path(
                    replace_in_str(str(old_relative_portion), self.name_map)
                )
            # print(f"{old_relative_portion=} {new_relative_portion=}")

            # get the destination path
            new_fp = self.new_root_fol / new_relative_portion
            # print(f".  {old_fp}\n > {new_fp}")

            # ensure the destination directory exists
            new_fp.parent.mkdir(parents=True, exist_ok=True)
            # copy the file
            shutil.copy(old_fp, new_fp)

            # break

    def update_files(self) -> None:
        """Update the contents of the files."""
        for new_fp in rglobber(self.new_root_fol, []):
            update_file_content(new_fp, self.name_map)

    def create_cred_file(self) -> None:
        """Create the credentials file."""
        self.cred_fp.parent.mkdir(parents=True, exist_ok=True)
        sample_cred = f"{self.name_map['PROJECT_NAME']}_SAMPLE_ENV_VAR=sample"
        self.cred_fp.write_text(sample_cred)

    def main(self) -> None:
        """Main method to execute the renaming process."""
        if not self.check_inputs():
            print("Exiting.")
            return
        self.copy_files()
        self.update_files()
        self.create_cred_file()
        print("Done.")


if __name__ == "__main__":
    r = Rename()
    r.main()
