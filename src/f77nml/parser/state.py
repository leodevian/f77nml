"""Parser states."""

from __future__ import annotations

import sys
from collections import OrderedDict
from typing import TYPE_CHECKING, Protocol

from f77nml.exceptions import UnexpectedTokenError
from f77nml.lexer import TokenType

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
    def process(self, context: ParserContext, token: Token) -> None:
        # Ignore space characters.
        if token.type is TokenType.NEWLINE or token.type is TokenType.SPACE:
            return

        if token.type is not TokenType.GROUP:
            raise UnexpectedTokenError(token)

        group_name = token.string.strip("$")
        context.data[group_name] = OrderedDict()
        context.data.move_to_end(group_name, last=True)
        context.state = SearchVariable()


class SearchVariable(ParserState):
    """The state for searching a variable."""

    @override
    def process(self, context: ParserContext, token: Token) -> None:
        # Ignore space characters.
        if token.type is TokenType.NEWLINE or token.type is TokenType.SPACE:
            return

        if token.type is TokenType.END:
            context.state = SearchGroup()
            return

        if token.type is not TokenType.VARIABLE:
            raise UnexpectedTokenError(token)

        variable_name = token.string
        context.current_group[variable_name] = None
        context.current_group.move_to_end(variable_name, last=True)
        context.state = SearchSubscript()


class SearchSubscript(ParserState):
    """The state for searching a subscript."""

    @override
    def process(self, context: ParserContext, token: Token) -> None: ...
