"""Token core."""

from dataclasses import dataclass
from functools import partial
import re
from qtpy.QtGui import QColor


Indirection = str
"""Token value that is a reference to another token."""


TokenValue = Indirection | QColor | float | int
"""Union of all possible token value types."""


@dataclass
class TokenValueWrapper:
    """Token runtime value wrapper type."""

    value: TokenValue


def define_token(value: TokenValue) -> TokenValueWrapper:
    """Factory function for defining a token.

    Mainly for internal use.
    """
    # TODO: add to token registry, check stack for module and var name?
    #   or use instance checking operator `is`?
    return TokenValueWrapper(value)


def resolve_token(token: str | TokenValue) -> TokenValue:
    """Resolve a token name to its value.

    If there are multiple token indirections, they are recursively
    resolved until a value is obtained.

    Example:
        from material_ui.tokens import md_comp_elevated_button as tokens
        value = resolve_token(tokens.container_color)
    """
    # Because the tokens system stores variables as values or names of
    # other tokens, first check if the tokens is a value already.
    if isinstance(token, (float, int, QColor)):
        return token
    match_result = re.match(r"(md\.(?:ref|comp|sys)\..+?)\.(.*)", token)
    if match_result is None:
        raise ValueError(f"Invalid token name: {token}")
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
    return resolve_token(token_value)


def override_token(token_name: str, value: TokenValue) -> None:
    """Override a token value in the global theme."""
    raise NotImplementedError()


to_python_name = partial(re.sub, r"[-\.]", "_")
"""Convert a token name to a valid Python identifier.

    Eg, md.comp.elevated-button.container-color ->
    md_comp_elevated_button_container_color
"""
