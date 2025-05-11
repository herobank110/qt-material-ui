"""Utilities."""

from qtpy.QtGui import QColor


_COMPONENT_STYLESHEET_RESET = {
    "background-color": "transparent",
    "border-radius": "0px",
    "border": "none",
    "margin": "0px",
    "padding": "0px",
}
"""Prevent Qt's unexpected behavior from inheriting parent's style."""


def convert_sx_to_qss(sx: dict[str, str]) -> str:
    """Convert a style dictionary to a Qt Style Sheet string.

    Args:
        sx: System property value.

    Returns:
        QSS string.
    """
    reset_sx = _COMPONENT_STYLESHEET_RESET | sx
    # TODO: resolve design tokens
    return ";".join(
        f"{key}:{_stringify_sx_value(value)}" for key, value in reset_sx.items()
    )


def _stringify_sx_value(value: str | QColor) -> str:
    """Convert a value to a string.

    Args:
        value: Value to convert.

    Returns:
        String representation of the value.
    """
    if isinstance(value, QColor):
        return f"rgba({value.red()},{value.green()},{value.blue()},{value.alpha()})"
    return value
