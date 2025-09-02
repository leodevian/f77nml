"""The parser."""

from __future__ import annotations

from collections import OrderedDict
from typing import TYPE_CHECKING, Any

from f77nml.exceptions import UnknownTokenError
from f77nml.lexer import TokenType, tokenize

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath, SupportsReadline

    from .state import ParserState


# noinspection PyAttributeOutsideInit
class Parser:
    """The parser class."""

    def __init__(self) -> None:
        """Initialize the parser."""
        self.reset()

    def transition_to(self, state: ParserState) -> None:
        """Transition to the given state.

        Args:
            state: The state to transition to.
        """
        self.state = state
        self.state.parser = self

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

                self.state.process(token)

            return self.data

        finally:
            self.reset()

    def reset(self) -> None:
        """Reset the parser.

        This method is called implicitly at instantiation time.
        """
        self.data: OrderedDict[str, OrderedDict[str, Any]] = OrderedDict()
        self.transition_to(...)


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
