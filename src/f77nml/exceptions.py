"""Exceptions and warnings."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from f77nml.lexer import Token


class UnknownTokenError(Exception):
    """An exception that formats an error message for unknown tokens."""

    def __init__(self, token: Token) -> None:
        """Initialize the exception.

        Args:
            token: The unknown token.
        """
        super().__init__(token)
        self.message = f"unknown token: {token.string!r}"
        self.token = token

    def __str__(self) -> str:
        """Return the error message."""
        return self.message
