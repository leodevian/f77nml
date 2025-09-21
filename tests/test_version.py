"""The test for the version attribute."""

from __future__ import annotations

import importlib.metadata

from f77nml import __version__


# https://packaging.python.org/discussions/single-source-version/#single-sourcing-the-project-version
def test_version() -> None:
    """Test that the version attribute matches the package version."""
    version = importlib.metadata.version("f77nml")
    assert __version__ == version
