# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "nox[uv]>=2025.2.9",
#   "uv>=0.8.6",
# ]
# ///
"""Task automation with Nox."""

from __future__ import annotations

import os
from pathlib import Path

import nox

nox.needs_version = ">=2025.2.9"
nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = (
    "lint",
    "typecheck",
    "tests",
)

PYPROJECT = nox.project.load_toml()
PROJECT_NAME = PYPROJECT["project"]["name"]
SUPPORTED_PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT)
DEFAULT_PYTHON_VERSION = Path(".python-version").read_text().rstrip()


@nox.session(python=SUPPORTED_PYTHON_VERSIONS, tags=["tests"])
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    uv_sync(
        "--no-editable",
        "--reinstall-package",
        PROJECT_NAME,
        "--group",
        "test",
        session=session,
    )
    tmp_dir = Path(session.create_tmp())

    if os.getenv("COVERAGE_FILE") is None:
        session.env["COVERAGE_FILE"] = str(tmp_dir / ".coverage")

    session.run("coverage", "erase")
    session.run(
        "coverage",
        "run",
        "-m",
        "pytest",
        *(
            session.posargs
            or (
                "--durations",
                "15",
                "-n",
                os.getenv("PYTEST_XDIST_AUTO_NUM_WORKERS") or "auto",
            )
        ),
    )
    session.run("coverage", "combine")
    session.run("coverage", "report")


@nox.session(python=DEFAULT_PYTHON_VERSION, tags=["checks"])
def lint(session: nox.Session) -> None:
    """Run pre-commit linting."""
    uv_sync("--group", "lint", session=session)
    session.run(
        "pre-commit",
        "run",
        "--all-files",
        *session.posargs,
        env={"FORCE_PRE_COMMIT_UV_PATCH": "1"},
    )


@nox.session(python=DEFAULT_PYTHON_VERSION, tags=["checks"])
def typecheck(session: nox.Session) -> None:
    """Typecheck Python code."""
    uv_sync(
        "--no-editable",
        "--reinstall-package",
        PROJECT_NAME,
        "--group",
        "type",
        session=session,
    )
    session.run("mypy", *(session.posargs or ("src", "tests")))


def uv_sync(*args: str, session: nox.Session) -> None:
    """Run ``uv sync`` to install dependencies."""
    session.run_install(
        "uv",
        "sync",
        "--locked",
        "--no-default-groups",
        *args,
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
            "UV_PYTHON": session.virtualenv.location,
        },
    )


if __name__ == "__main__":
    nox.main()
