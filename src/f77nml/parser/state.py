"""Parser states."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Protocol

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

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
