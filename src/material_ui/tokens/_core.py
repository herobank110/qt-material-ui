"""Token core."""

from functools import partial
import re
from qtpy.QtGui import QColor


Indirection = str
"""Token value that is a reference to another token."""


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


to_python_name = partial(re.sub, r"[-\.]", "_")
"""Convert a token name to a valid Python identifier.

    Eg, md.comp.elevated-button.container-color ->
    md_comp_elevated_button_container_color
"""
