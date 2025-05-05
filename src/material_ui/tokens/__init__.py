"""Design Token system.

Hardcoded values are available for all tokens. They can also be
overridden with an exported theme from Material Theme Builder plugin for
Figma, or dynamically generated.
"""

from qtpy.QtGui import QColor


TokenValue = str | QColor | int


def resolve_token(token_name: str) -> TokenValue:
    """Resolve a token name to its value.

    If there are multiple token indirections, they are recursively
    resolved until a value is obtained.
    """
    raise NotImplementedError()


def override_token(token_name: str, value: TokenValue) -> None:
    """Override a token value in the global theme."""
    raise NotImplementedError()
