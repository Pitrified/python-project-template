"""Load environment variables from .env file."""

from pathlib import Path

from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from .env file."""
    # standard place to store credentials outside of version control and folder
    cred_path = Path.home() / "cred" / "python-project-template" / ".env"
    if cred_path.exists():
        load_dotenv(dotenv_path=cred_path)
