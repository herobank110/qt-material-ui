"""Menu component.

A popup menu that opens at a specific location and displays a list of
selectable items.
"""

from qtpy.QtCore import QEasingCurve, QMargins, QPoint, Qt

from material_ui._component import Component, Signal, effect, use_state
from material_ui._lab import DropShadow
from material_ui.layout_basics import Row, Stack
from material_ui.shape import Shape
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

    def open(self, anchor_widget: Component) -> None:
        """Open the menu anchored to a specific widget.

        Args:
            anchor_widget: The widget to anchor the menu to.
        """
        pos = anchor_widget.mapToGlobal(QPoint(0, anchor_widget.height()))
        pos -= QPoint(0, _CONTAINER_DROP_SHADOW_SPACE)
        self.move(pos)
        self.show()

    @effect(Component.children)
    def _layout_menu_items(self) -> None:
        items = self.findChildren(
            MenuItem,
            options=Qt.FindChildOption.FindDirectChildrenOnly,
        )
        for item in items:
            self._stack.add_widget(item)


class MenuItem(Component):
    """A single menu item."""

    text = use_state("")
    """Text displayed in the menu item."""

    on_click: Signal
    """Emitted with the menu item is clicked."""

    _state_layer_opacity = use_state(
        0.0,
        transition=200,
        easing=QEasingCurve.Type.InOutCubic,
    )

    def __init__(self) -> None:
        super().__init__()
        self.setFixedHeight(resolve_token(tokens.list_item_container_height))

        row = Row()
        row.alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        row.margins = QMargins(
            _LEFT_RIGHT_PADDING,
            0,
            _LEFT_RIGHT_PADDING,
            0,
        )

        # TODO: add leading and trailing icons to row

        self._label = Typography()
        self._label.text = self.text
        self._label.font_family = tokens.list_item_label_text_font
        self._label.font_size = tokens.list_item_label_text_size
        self._label.font_weight = tokens.list_item_label_text_weight
        row.add_widget(self._label)

        self._state_layer = Shape()
        self._state_layer.setParent(self)
        self._state_layer.opacity = self._state_layer_opacity

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

    @effect(_state_layer_opacity)
    def f(self):
        print(self._state_layer_opacity)
