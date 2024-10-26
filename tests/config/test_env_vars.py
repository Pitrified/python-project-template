"""Test that the environment variables are available."""

import os

import pytest


def test_env_vars() -> None:
    """The environment var PROJECT_NAME_SAMPLE_ENV_VAR is available."""
    assert "PROJECT_NAME_SAMPLE_ENV_VAR" in os.environ
    assert os.environ["PROJECT_NAME_SAMPLE_ENV_VAR"] == "sample"
