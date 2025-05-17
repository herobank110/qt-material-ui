"""Token core."""

import contextlib
from dataclasses import dataclass
from functools import partial
import re
from qtpy.QtGui import QColor


Indirection = str
"""Token value that is a reference to another token."""


TokenValue = QColor | float | int
"""Union of underlying token value types (excluding Indirections)."""


@dataclass
class DesignToken:
    """Token runtime value wrapper type."""

    value: Indirection | TokenValue

    def __hash__(self):
        # Allow the token to be used as a dictionary key.
        # TODO: fix it to use @dataclass(unsafe_hash=True) instead
        # QColor isn't hashable, so convert to string
        return hash(repr(self.value))


def define_token(value: TokenValue) -> DesignToken:
    """Factory function for defining a token.

    Mainly for internal use.
    """
    # TODO: add to token registry, check stack for module and var name?
    #   or use instance checking operator `is`?
    return DesignToken(value)


def resolve_token(token: DesignToken) -> TokenValue:
    """Resolve a token to its underlying value.

    If there are multiple token indirections, they are recursively
    resolved until a value is obtained.

    Args:
        token: The token to resolve.

    Returns:
        The value represented by the token.

    Example:
        from material_ui.tokens import md_comp_elevated_button as tokens
        value = resolve_token(tokens.container_color)
    """
    return find_root_token(token).value


def find_root_token(token: DesignToken) -> DesignToken:
    """Resolve a token to the last token in the chain of indirection.

    Consider `resolve_token` if just trying to get the underlying token
    value. This function is mainly useful for using tokens as hash keys.

    Args:
        token: The token to resolve.

    Returns:
        The last token in the chain of indirections.
    """
    # Because the tokens system stores variables as values or names of
    # other tokens, first check if the tokens is a value already.
    if not _is_indirection(token):
        return token
    indirection = _resolve_indirection(token.value)
    if not indirection:
        raise ValueError(f"Unable to resolve token indirection: {token.value}")
    # Continue recursively to check until a value is obtained.
    return find_root_token(indirection)


# TODO: make proper indirection class instead of hardcoded string check
_NOT_INDIRECTION = {
    "SHAPE_FAMILY_CIRCULAR",
    "SHAPE_FAMILY_ROUNDED_CORNERS",
    "Roboto"
}


def _is_indirection(token: DesignToken) -> bool:
    """Check if the token is an indirection.

    Args:
        token: The token to check.

    Returns:
        True if the token is an indirection, False if a value.
    """
    is_value_type = isinstance(token.value, TokenValue)
    return not is_value_type and token.value not in _NOT_INDIRECTION


def _resolve_indirection(value: Indirection) -> DesignToken | None:
    if match_result := re.match(r"(md\.(?:ref|comp|sys)\..+?)\.(.*)", value):
        py_module_name = to_python_name(match_result.group(1))
        var_name = to_python_name(match_result.group(2))
        with contextlib.suppress(ImportError):
            module = __import__(f"material_ui.tokens.{py_module_name}")
            with contextlib.suppress(AttributeError):
                token = getattr(getattr(module.tokens, py_module_name), var_name)
                if isinstance(token, DesignToken):
                    return token
    return None


def override_token(token_name: str, value: TokenValue) -> None:
    """Override a token value in the global theme."""
    raise NotImplementedError()


to_python_name = partial(re.sub, r"[-\.]", "_")
"""Convert a token name to a valid Python identifier.

    Eg, md.comp.elevated-button.container-color ->
    md_comp_elevated_button_container_color
"""
