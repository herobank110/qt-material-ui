"""Token core."""

import contextlib
import re
from dataclasses import dataclass
from functools import partial
from typing import TypeVar, cast

from qtpy.QtGui import QColor

Indirection = str
"""Token value that is a reference to another token."""


TokenValue = QColor | float | int
"""Union of underlying token value types (excluding Indirections)."""


@dataclass
class DesignToken:
    """Token runtime value wrapper type."""

    value: Indirection | TokenValue

    def __hash__(self) -> int:
        # Allow the token to be used as a dictionary key.
        # TODO: fix it to use @dataclass(unsafe_hash=True) instead
        # QColor isn't hashable, so convert to string
        return hash(repr(self.value))


_token_registry: set[DesignToken] = set()
"""Global registry for all registered tokens."""


def define_token(value: TokenValue | Indirection) -> DesignToken:
    """Factory function for defining a token and registering it by name.

    Mainly for internal use.
    """
    ret_val = DesignToken(value)
    _token_registry.add(ret_val)
    return ret_val


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
    # Assume the root token is a value not indirection.
    return cast("TokenValue", find_root_token(token).value)


_T = TypeVar("_T")


def resolve_token_or_value(token_or_value: _T | DesignToken) -> _T:
    """If a token is passed, resolve it. Otherwise, return the value itself."""
    if isinstance(token_or_value, DesignToken):
        resolved = resolve_token(token_or_value)
        return cast("_T", resolved)
    return token_or_value


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
    indirection = _resolve_indirection(cast("Indirection", token.value))
    if not indirection:
        msg = f"Unable to resolve token indirection: {token.value}"
        raise ValueError(msg)
    # Continue recursively to check until a value is obtained.
    return find_root_token(indirection)


# TODO: make proper indirection class instead of hardcoded string check
_NOT_INDIRECTION = {"SHAPE_FAMILY_CIRCULAR", "SHAPE_FAMILY_ROUNDED_CORNERS", "Roboto"}


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


def override_token(token: DesignToken, value: TokenValue) -> None:
    """Override a token value in the global theme and notify listeners."""
    token.value = value
    # Local import to avoid circular import.
    from material_ui.theming.theme_hook import ThemeHook

    ThemeHook.get().on_change.emit()


to_python_name = partial(re.sub, r"[-\.]", "_")
"""Convert a token name to a valid Python identifier.

    Eg, md.comp.elevated-button.container-color ->
    md_comp_elevated_button_container_color
"""
