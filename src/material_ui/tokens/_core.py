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
    match_result = re.match(r"(md\.(?:ref|comp|sys)\..+?)\.(.*)", token_name)
    if match_result is None:
        raise ValueError(f"Invalid token name: {token_name}")
    py_module_name = to_python_name(match_result.group(1))
    var_name = to_python_name(match_result.group(2))
    try:
        module = __import__(f"material_ui.tokens.{py_module_name}")
    except ImportError as e:
        raise ImportError(f"Module {py_module_name} not found") from e
    try:
        token_value = getattr(getattr(module.tokens, py_module_name), var_name)
    except AttributeError as e:
        raise AttributeError(f"Token {var_name} not found in {py_module_name}") from e
    # TODO: resolve indirections
    # if isinstance(token_value, Indirection):
    return token_value


def override_token(token_name: str, value: TokenValue) -> None:
    """Override a token value in the global theme."""
    raise NotImplementedError()


to_python_name = partial(re.sub, r"[-\.]", "_")
"""Convert a token name to a valid Python identifier.

    Eg, md.comp.elevated-button.container-color ->
    md_comp_elevated_button_container_color
"""
