"""Menu component.

A popup menu that opens at a specific location and displays a list of
selectable items.
"""

from typing import cast

from PySide6.QtGui import QMouseEvent
from qtpy.QtCore import QEasingCurve, QMargins, QPoint, Qt, QTimer

from material_ui._component import Component, effect, use_state
from material_ui._lab import DropShadow
from material_ui.icon import Icon
from material_ui.layout_basics import Row, Stack
from material_ui.ripple import Ripple
from material_ui.shape import Shape
from material_ui.theming.theme_hook import ThemeHook
from material_ui.tokens import md_comp_menu as tokens
from material_ui.tokens._utils import resolve_token, resolve_token_or_value
from material_ui.typography import Typography

_CONTAINER_DROP_SHADOW_SPACE = 10
"""Extra space around the menu container to accommodate the drop shadow."""

_DROP_SHADOW_MARGIN = QMargins(
    _CONTAINER_DROP_SHADOW_SPACE,
    _CONTAINER_DROP_SHADOW_SPACE,
    _CONTAINER_DROP_SHADOW_SPACE,
    _CONTAINER_DROP_SHADOW_SPACE,
)
_DIVIDER_MARGINS = QMargins(0, 8, 0, 8)
_CONTAINER_WIDTH_MIN = 112
_CONTAINER_WIDTH_MAX = 280
_LEFT_RIGHT_PADDING = 12
_GAP_BETWEEN_ELEMENTS_IN_ITEM = 12


class Menu(Component):
    """A popup menu that displays a list of selectable items."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Popup  # automatically closed on click outside
            | Qt.WindowType.NoDropShadowWindowHint  # use custom drop shadow
            | Qt.WindowType.FramelessWindowHint,  # prevent border
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
        )
        self.setMinimumWidth(_CONTAINER_WIDTH_MIN)
        self.setMaximumWidth(_CONTAINER_WIDTH_MAX)

        container = Shape()
        container.color = tokens.container_color
        container.corner_shape = tokens.container_shape

        drop_shadow = DropShadow()
        drop_shadow.shadow_color = tokens.container_shadow_color
        drop_shadow.elevation = tokens.container_elevation
        drop_shadow.setParent(container)
        container.setGraphicsEffect(drop_shadow)

        self._stack = Stack(margins=_DIVIDER_MARGINS)
        container.overlay_widget(self._stack)

        self.overlay_widget(container, margins=_DROP_SHADOW_MARGIN)

    def open(
        self,
        anchor_widget: Component,
        *,
        stretch_width: bool = False,
    ) -> None:
        """Open the menu anchored to a specific widget.

        Args:
            anchor_widget: The widget to anchor the menu to.
            stretch_width: Whether to fit the width of the anchor
                widget.
        """
        pos = anchor_widget.mapToGlobal(QPoint(0, anchor_widget.height()))
        pos -= QPoint(_CONTAINER_DROP_SHADOW_SPACE, _CONTAINER_DROP_SHADOW_SPACE)
        self.move(pos)
        if stretch_width:
            self.setFixedWidth(anchor_widget.width() + _CONTAINER_DROP_SHADOW_SPACE * 2)
        self.show()

    def close_menu(self) -> None:
        """Close the menu."""
        self.destroy()

    @effect(Component.children)
    def _layout_menu_items(self) -> None:
        items = self.findChildren(
            MenuItem,
            options=Qt.FindChildOption.FindDirectChildrenOnly,
        )
        for item in items:
            item.clicked.connect(self._on_click_menu_item)
            self._stack.add_widget(item)

    def _on_click_menu_item(self) -> None:
        """Close menu when clicked something."""
        # Put a delay so the ripple can be enjoyed.
        QTimer.singleShot(50, self.close_menu)


class MenuItem(Component):
    """A single menu item."""

    text = use_state("")
    """Text displayed in the menu item."""

    leading_icon = use_state(cast("Icon | None", None))
    """Icon to go at the start of the item."""

    _state_layer_opacity = use_state(
        0.0,
        transition=70,
        easing=QEasingCurve.Type.InOutCubic,
    )

    def __init__(self) -> None:
        super().__init__()
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(resolve_token(tokens.list_item_container_height))

        row = Row()
        row.alignment = Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignVCenter
        row.margins = QMargins(_LEFT_RIGHT_PADDING, 0, _LEFT_RIGHT_PADDING, 0)
        row.gap = _GAP_BETWEEN_ELEMENTS_IN_ITEM

        self._leading_icon_wrapper = Component()
        row.add_widget(self._leading_icon_wrapper)

        self._label = Typography()
        self._label.text = self.text
        self._label.font_family = tokens.list_item_label_text_font
        self._label.font_size = tokens.list_item_label_text_size
        self._label.font_weight = tokens.list_item_label_text_weight
        self._label.alignment = (
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignVCenter
        )
        row.add_widget(self._label)

        self._state_layer = Shape()
        self._state_layer.setParent(self)
        self._state_layer.opacity = self._state_layer_opacity

        self._ripple = Ripple()
        self._ripple.color = tokens.list_item_pressed_state_layer_color
        self._ripple.clip_half_rounded = False
        self._state_layer.overlay_widget(self._ripple)

        self.overlay_widget(row)

    @effect(Component.size)
    def _apply_state_label_size(self) -> None:
        self._state_layer.resize(self.size())

    @effect(Component.hovered, Component.pressed)
    def _apply_state_layer_color(self) -> None:
        self._state_layer.color = (
            tokens.list_item_pressed_state_layer_color
            if self.pressed
            else tokens.list_item_hover_state_layer_color
        )
        self._state_layer_opacity = resolve_token_or_value(
            tokens.list_item_pressed_state_layer_opacity
            if self.pressed
            else tokens.list_item_hover_state_layer_opacity
            if self.hovered
            else 0.0,
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Override to handle ripple."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._ripple.ripple_origin = event.position()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Override to handle ripple."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._ripple.ripple_origin = None
        return super().mouseReleaseEvent(event)

    @effect(leading_icon)
    def _place_leading_icon(self) -> None:
        """Place the leading icon in the menu item."""
        # Delete previous icon if exists.
        if prev_icon := self._leading_icon_wrapper.findChild(Icon):
            if prev_icon is self.leading_icon:
                return  # Nothing to do.
            prev_icon.setParent(None)
        if self.leading_icon is None:
            # No icon needed.
            return
        # Show new icon.
        self._leading_icon_wrapper.overlay_widget(self.leading_icon)

    @effect(leading_icon, ThemeHook)
    def _apply_leading_icon_properties(self) -> None:
        icon = self.leading_icon
        if icon is None:
            return
        icon.font_size = tokens.list_item_with_leading_icon_leading_icon_size
        icon.color = tokens.list_item_with_leading_icon_leading_icon_color
