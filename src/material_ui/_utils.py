"""Utilities."""

from qtpy.QtGui import QColor
from material_ui.tokens import DesignToken, resolve_token


StyleDictValue = str | QColor | DesignToken
"""Union of values that can be used in a style dictionary."""

# TODO: use a typed dict for completion on keys and type checking on values
StyleDict = dict[str, StyleDictValue]
"""Dictionary of styles."""


_COMPONENT_STYLESHEET_RESET: StyleDict = {
    "background-color": "transparent",
    "border-radius": "0px",
    "border": "none",
    "margin": "0px",
    "padding": "0px",
}
"""Prevent Qt's unexpected behavior from inheriting parent's style."""


def convert_sx_to_qss(sx: StyleDict) -> str:
    """Convert a style dictionary to a Qt Style Sheet string.

    Args:
        sx: System property value.

    Returns:
        QSS string.
    """
    sx = _COMPONENT_STYLESHEET_RESET | sx
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
    return value
