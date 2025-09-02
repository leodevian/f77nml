"""Parser states."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, override

if TYPE_CHECKING:
    from f77nml.lexer import Token

    from . import ParserContext


class ParserState(Protocol):
    """The interface for parser states."""

    def process(self, context: ParserContext, token: Token) -> None:
        """Process a token.

        Args:
            context: The current context.
            token: The token to process.
        """
        ...


class SearchGroup(ParserState):
    """The state for searching a new group."""

    @override
    def process(self, context: ParserContext, token: Token) -> None: ...
