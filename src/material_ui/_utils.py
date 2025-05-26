"""Utilities."""

from collections.abc import Mapping

from qtpy.QtGui import QColor

from material_ui.tokens import DesignToken, resolve_token

StyleDictValue = str | int | float | QColor | DesignToken
"""Union of values that can be used in a style dictionary."""

# TODO: use a typed dict for completion on keys and type checking on values
StyleDict = Mapping[str, StyleDictValue]
"""Dictionary of styles."""


def convert_sx_to_qss(sx: StyleDict) -> str:
    """Convert a style dictionary to a Qt Style Sheet string.

    Args:
        sx: System property value.

    Returns:
        QSS string.
    """
    return ";".join(f"{key}:{_stringify_sx_value(value)}" for key, value in sx.items())


def _stringify_sx_value(value: StyleDictValue) -> str:
    """Convert a value to a string.

    Design tokens are resolved to the underlying values.

    Args:
        value: Value to convert.

    Returns:
        String representation of the value.
    """
    # First things first, resolve the design tokens.
    if isinstance(value, DesignToken):
        value = resolve_token(value)
    # Then convert the special values to strings.
    if isinstance(value, QColor):
        return f"rgba({value.red()},{value.green()},{value.blue()},{value.alpha()})"
    if isinstance(value, int):
        return f"{value}px"
    if isinstance(value, float):
        return f"{value}"
    return value


undefined = object()
"""A special token to indicate an undefined value."""
