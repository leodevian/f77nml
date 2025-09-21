"""The version attribute."""

from __future__ import annotations

import importlib.resources


def get_version() -> str:
    """Read ``VERSION.txt`` and return its contents.

    Returns:
        The version string.
    """
    return (
        (importlib.resources.files("f77nml") / "VERSION.txt")
        .read_text(encoding="utf-8")
        .rstrip()
    )


__version__ = get_version()
