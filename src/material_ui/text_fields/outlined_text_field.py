"""Outlined text field component."""

from qtpy.QtCore import QMargins, QPoint, Qt

from material_ui._component import Component, effect
from material_ui.layout_basics import Row
from material_ui.shape import Shape
from material_ui.text_fields._base_text_field import BaseTextField
from material_ui.tokens import md_comp_outlined_text_field as tokens
from material_ui.tokens import md_sys_color
from material_ui.theming.theme_hook import ThemeHook

_LINE_EDIT_POS = QPoint(16, 18)


class OutlinedTextField(BaseTextField):
    """Outlined text field component."""

    _FLOATING_LABEL_POS = QPoint(12, 0)
    _RESTING_LABEL_POS = QPoint(16, 24)

    def __init__(self) -> None:
        super().__init__()
        self._container = Shape()
        self._container.corner_shape = tokens.container_shape
        self._container.opacity = 0.0
        self._container.sx = {
            **self._container.sx,
            "border-width": tokens.outline_width,
            "border-style": "solid",
        }
        self._container.setParent(self)

        self._focus_outline = Shape()
        self._focus_outline.corner_shape = tokens.container_shape
        self._focus_outline.visible = self.focused
        self._focus_outline.opacity = 0.0
        self._focus_outline.sx = {
            **self._focus_outline.sx,
            "border-width": tokens.focus_outline_width,
            "border-style": "solid",
            "border-color": tokens.focus_outline_color,
        }
        self._focus_outline.setParent(self)

        self._resting_label.setParent(self)
        self._resting_label.font_family = tokens.label_text_font
        self._resting_label.font_size = tokens.label_text_size
        self._resting_label.font_weight = tokens.label_text_weight

        self._floating_label.setParent(self)
        self._floating_label.font_family = tokens.label_text_font
        self._floating_label.font_size = tokens.label_text_populated_size
        self._floating_label.font_weight = tokens.label_text_weight
        self._floating_label.sx = {
            **self._floating_label.sx,
            # TODO: split outline into 3 parts to make it all transparent
            "background-color": md_sys_color.background,
            "margin": "0 4px",
        }

        line_edit_wrapper = Component()
        line_edit_wrapper.sx = {
            "color": tokens.input_text_color,
            "font-family": tokens.input_text_font,
            "font-size": tokens.input_text_size,
        }
        line_edit_wrapper.setParent(self._container)
        line_edit_wrapper.move(_LINE_EDIT_POS)
        self._line_edit.setParent(line_edit_wrapper)

        # Set up trailing icon wrapper position
        self._trailing_icon_wrapper.setParent(self._container)

    @effect(Component.hovered)
    def _apply_container_border(self) -> None:
        color = tokens.hover_outline_color if self.hovered else tokens.outline_color
        self._container.sx = {**self._container.sx, "border-color": color}

    @effect(Component.size, BaseTextField.trailing_icon)
    def _resize_elements(self) -> None:
        self._container.resize(self.size().shrunkBy(QMargins(0, self._TOP_SPACE, 0, 0)))
        self._container.move(QPoint(0, self._TOP_SPACE))
        self._focus_outline.resize(self._container.size())
        self._focus_outline.move(QPoint(0, self._TOP_SPACE))
        
        # Position trailing icon if present
        if self.trailing_icon is not None:
            from material_ui.tokens._utils import resolve_token
            icon_size = resolve_token(tokens.trailing_icon_size)
            icon_margin = 16  # Distance from right edge
            icon_x = self._container.width() - icon_size - icon_margin
            icon_y = (self._container.height() - icon_size) // 2
            self._trailing_icon_wrapper.setFixedSize(icon_size, icon_size)
            self._trailing_icon_wrapper.move(icon_x, icon_y)

    @effect(BaseTextField.trailing_icon, ThemeHook)
    def _apply_trailing_icon_properties(self) -> None:
        """Apply styling to trailing icon based on current state."""
        icon = self.trailing_icon
        if icon is None:
            return
        from material_ui.tokens._utils import resolve_token
        icon.font_size = resolve_token(tokens.trailing_icon_size)
        
        # Apply state-based color
        if self.focused:
            icon.color = tokens.focus_trailing_icon_color
        elif self.hovered:
            icon.color = tokens.hover_trailing_icon_color
        else:
            icon.color = tokens.trailing_icon_color

    @effect(Component.focused)
    def _apply_label_color(self) -> None:
        color = (
            tokens.focus_label_text_color if self.focused else tokens.label_text_color
        )
        self._floating_label.sx = {**self._floating_label.sx, "color": color}
        self._resting_label.sx = {**self._resting_label.sx, "color": color}

    @effect(Component.focused, Component.hovered)
    def _update_trailing_icon_color(self) -> None:
        """Update trailing icon color when focus or hover state changes."""
        if self.trailing_icon is None:
            return
        # Apply state-based color
        if self.focused:
            self.trailing_icon.color = tokens.focus_trailing_icon_color
        elif self.hovered:
            self.trailing_icon.color = tokens.hover_trailing_icon_color
        else:
            self.trailing_icon.color = tokens.trailing_icon_color
