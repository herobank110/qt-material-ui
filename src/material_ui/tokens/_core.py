"""Token core."""

from dataclasses import dataclass
from qtpy.QtGui import QColor


@dataclass
class Indirection:
    """Token value that is a reference to another token."""

    name: str


TokenValue = Indirection | QColor | float | int
"""Union of all possible token value types."""


def resolve_token(token_name: str) -> TokenValue:
    """Resolve a token name to its value.

    If there are multiple token indirections, they are recursively
    resolved until a value is obtained.
    """
    raise NotImplementedError()


def override_token(token_name: str, value: TokenValue) -> None:
    """Override a token value in the global theme."""
    raise NotImplementedError()
