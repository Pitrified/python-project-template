"""Script to rename a project.

1. Input the new project and repo names.
1. Copy the files to the new project name.
1. Update the contents of the files.
1. Create a credentials file.
"""

from collections.abc import Generator
from pathlib import Path
import shutil
from typing import Annotated

from rich import print as rprint
import typer

app = typer.Typer()


def replace_in_str(s: str, name_map: dict[str, str]) -> str:
    """Replace all instances of project_name (and variations) in a string."""
    for old, new in name_map.items():
        s = s.replace(old, new)
    return s


def rglobber(fol: Path, skip_fols: list[str]) -> Generator[Path]:
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

    def __init__(self, project_name: str, repo_name: str | None) -> None:
        """Initialize the Rename class."""
        self.project_name = project_name
        self.repo_name = repo_name
        self.build_name_map()
        self.build_roots()
        self.build_cred_fp()

    def build_name_map(self) -> None:
        """Build the name map."""
        pieces = self.project_name.split("_")
        kebab_case = "-".join(pieces)
        camel_case = "".join([p.capitalize() for p in pieces])
        pretty = " ".join(pieces).capitalize()

        if self.repo_name is None:
            self.repo_name = kebab_case

        self.name_map = {
            "project_name": self.project_name,
            "PROJECT_NAME": self.project_name.upper(),
            "project-name": kebab_case,
            "ProjectName": camel_case,
            "Project name": pretty,
            "python-project-template": self.repo_name,
        }
        rprint("[bold]Name map:[/bold]")
        rprint(self.name_map)

    def build_roots(self) -> None:
        """Build the roots of the old and new projects."""
        self.old_root_fol = Path(__file__).parents[1].resolve()
        # self.repo_name is guaranteed to be set by build_name_map
        if self.repo_name is None:
            msg = "repo_name not set"
            raise ValueError(msg)
        self.new_root_fol = self.old_root_fol.parent / self.repo_name
        rprint(f"Will init the project in [green]{self.new_root_fol}[/green]")

    def build_cred_fp(self) -> None:
        """Build the credentials file path."""
        # self.repo_name is guaranteed to be set by build_name_map
        if self.repo_name is None:
            msg = "repo_name not set"
            raise ValueError(msg)
        self.cred_fp = Path.home() / "cred" / self.repo_name / ".env"

    def check_inputs(self) -> None:
        """Check that the project name is correct and not already in use."""
        if self.new_root_fol.exists():
            rprint(f"[red]Error: {self.new_root_fol} already exists.[/red]")
            raise typer.Exit(code=1)
        if self.cred_fp.exists():
            rprint(f"[red]Error: {self.cred_fp} already exists.[/red]")
            raise typer.Exit(code=1)

        if not typer.confirm("Is the above information correct?"):
            rprint("Exiting.")
            raise typer.Exit

    def copy_files(self) -> None:
        """Copy files to the new project name."""
        rprint("Copying files...")
        # skip these directories
        skip_fols = [
            "__pycache__",
            ".pytest_cache",
            ".ruff_cache",
            ".git",
            ".venv",
            # "meta",
        ]
        # skip these files
        skip_portions = [
            "README.md",
            "poetry.lock",
            "uv.lock",
            "meta/rename_project.py",
            "pyproject.toml",
        ]
        # special cases to rename
        special_portions = {
            "final_resources/README.md": "README.md",
            "final_resources/pyproject.toml": "pyproject.toml",
            "meta/README.md": "README_POST_CREATE.md",
        }

        for old_fp in rglobber(self.old_root_fol, skip_fols):
            # get the portion of the source path relative to the root
            old_relative_portion = old_fp.relative_to(self.old_root_fol)

            # skip certain files
            if str(old_relative_portion) in skip_portions:
                continue

            # change the file name in the relative portion
            if str(old_relative_portion) in special_portions:
                # change the file name in a custom way
                new_relative_portion = Path(special_portions[str(old_relative_portion)])
            else:
                # change the file name in the standard way with the name map
                new_relative_portion = Path(
                    replace_in_str(str(old_relative_portion), self.name_map),
                )

            # get the destination path
            new_fp = self.new_root_fol / new_relative_portion

            # ensure the destination directory exists
            new_fp.parent.mkdir(parents=True, exist_ok=True)
            # copy the file
            shutil.copy(old_fp, new_fp)

    def update_files(self) -> None:
        """Update the contents of the files."""
        rprint("Updating files...")
        for new_fp in rglobber(self.new_root_fol, []):
            update_file_content(new_fp, self.name_map)

    def create_cred_file(self) -> None:
        """Create the credentials file."""
        rprint("Creating credentials file...")
        self.cred_fp.parent.mkdir(parents=True, exist_ok=True)
        sample_cred = f"{self.name_map['PROJECT_NAME']}_SAMPLE_ENV_VAR=sample"
        self.cred_fp.write_text(sample_cred)

    def run(self) -> None:
        """Run the renaming process."""
        self.check_inputs()
        self.copy_files()
        self.update_files()
        self.create_cred_file()
        rprint("[bold green]Done.[/bold green]")


@app.command()
def main(
    project_name: Annotated[
        str, typer.Argument(help="The new project name (e.g. my_new_project)")
    ],
    repo_name: Annotated[
        str | None,
        typer.Option(
            help=(
                "The new repository name (e.g. my-new-project). "
                "Defaults to kebab-case of project_name."
            )
        ),
    ] = None,
) -> None:
    """Rename the project template to a new project name."""
    rename = Rename(project_name, repo_name)
    rename.run()


if __name__ == "__main__":
    app()
