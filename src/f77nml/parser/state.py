"""Parser states."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from f77nml.lexer import Token

    from . import Parser


class ParserState(Protocol):
    """The interface for parser states."""

    parser: Parser

    def process(self, token: Token) -> None:
        """Process a token.

        Args:
            token: The token to process.
        """
        ...
