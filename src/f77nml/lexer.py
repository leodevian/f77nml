"""The lexer."""

from __future__ import annotations

import enum
import re
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Generator

    from _typeshed import SupportsReadline


class TokenType(enum.Enum):
    """The enumeration of token types."""

    EOF = enum.auto()
    GROUP = enum.auto()
    END = enum.auto()
    VARIABLE = enum.auto()
    COMMA = enum.auto()
    COLON = enum.auto()
    LPAREN = enum.auto()
    RPAREN = enum.auto()
    EQUALITY = enum.auto()
    REPEAT = enum.auto()
    LOGICAL = enum.auto()
    NUMBER = enum.auto()
    STRING = enum.auto()
    SPACE = enum.auto()
    COMMENT = enum.auto()
    UNKNOWN = enum.auto()


PATTERNS = (
    (TokenType.GROUP, r"\$[a-zA-Z][a-zA-Z0-9_]*"),
    (TokenType.END, r"\$(END)?"),
    (TokenType.VARIABLE, r"[a-zA-Z][a-zA-Z0-9_]*"),
    (TokenType.COMMA, r","),
    (TokenType.COLON, r":"),
    (TokenType.LPAREN, r"\("),
    (TokenType.RPAREN, r"\)"),
    (TokenType.EQUALITY, r"="),
    (TokenType.REPEAT, r"[0-9]+\*"),
    (TokenType.LOGICAL, r"\.(TRUE|FALSE)\."),
    (TokenType.NUMBER, r"[+-]?\d+(\.\d*)?(E?[+-]?\d+)?"),
    (TokenType.STRING, r"('([^']|'')*'|\"[^\"]*\")"),
    (TokenType.SPACE, r"[ \t\r\n]+"),
    (TokenType.COMMENT, r"![^\n]*"),
    (TokenType.UNKNOWN, r"."),
)


class Token(NamedTuple):
    """The token class."""

    type: TokenType
    """The token type."""

    string: str
    """The match string."""


def tokenize(
    stream: SupportsReadline[str],
    *,
    start: int = 1,
    size: int = -1,
) -> Generator[Token]:
    """Return a token generator from a stream.

    Args:
        stream: The stream to tokenize.
        start: The start position on each line.
        size: The length of each line.

    Returns:
        Token generator.
    """
    regex = re.compile(
        "|".join(
            f"(?P<{token_type.name}>{pattern})" for token_type, pattern in PATTERNS
        ),
        re.IGNORECASE,
    )

    while line := stream.readline(size):
        # Column one is totally ignored.
        for match in regex.finditer(line, start):
            # All capture groups are named.
            token_type = TokenType[match.lastgroup]  # type: ignore[misc]
            string = match.group(token_type.name)

            # Ignore comments.
            if token_type is TokenType.COMMENT:
                continue

            yield Token(type=token_type, string=string)

    yield Token(type=TokenType.EOF, string="")
