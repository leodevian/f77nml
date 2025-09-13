"""The parser."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from f77nml.exceptions import UnknownTokenError
from f77nml.lexer import TokenType, tokenize

from .state import SearchGroup

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath, SupportsReadline

    from .state import ParserState


@dataclass(slots=True)
class ParserContext:
    """The context class."""

    state: ParserState = field(default_factory=SearchGroup)
    """The current state."""

    data: OrderedDict[str, OrderedDict[str, Any]] = field(default_factory=OrderedDict)
    """The data."""

    @property
    def current_group(self) -> OrderedDict[str, Any]:
        """Return the current group.

        Returns:
            The current group.
        """
        return next(reversed(self.data.values()))


# noinspection PyAttributeOutsideInit
class Parser:
    """The parser class."""

    def __init__(self) -> None:
        """Initialize the parser."""
        self.reset()

    def parse(
        self,
        stream: SupportsReadline[str],
        *,
        start: int = 1,
        size: int = -1,
    ) -> OrderedDict[str, OrderedDict[str, Any]]:
        """Return a dictionary from a stream containing FORTRAN 77 NAMELIST I/O.

        Args:
            stream: The stream to parse.
            start: The start position on each line.
            size: The length of each line.

        Returns:
            A dictionary containing the parsed data.
        """
        try:
            for token in tokenize(stream, start=start, size=size):
                if token.type is TokenType.UNKNOWN:
                    raise UnknownTokenError(token)

                self.context.state.process(self.context, token)

            return self.context.data

        finally:
            self.reset()

    def reset(self) -> None:
        """Reset the parser's context.

        This method is called implicitly at instantiation time.
        """
        self.context = ParserContext()


def read(
    path: StrOrBytesPath,
    *,
    encoding: str | None = None,
    start: int = 1,
    size: int = -1,
) -> OrderedDict[str, OrderedDict[str, Any]]:
    """Return a dictionary from FORTRAN 77 NAMELIST I/O.

    Args:
        path: The path to the FORTRAN 77 NAMELIST I/O to parse.
        encoding: The encoding to use.
        start: The start position on each line.
        size: The length of each line.

    Returns:
        A dictionary containing the parsed data.
    """
    parser = Parser()

    with open(path, encoding=encoding) as stream:
        return parser.parse(stream, start=start, size=size)
