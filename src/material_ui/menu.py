"""Menu component.

A popup menu that opens at a specific location and displays a list of
selectable items.
"""

from qtpy.QtCore import QMargins, QPoint, Qt

from material_ui._component import Component, Signal, use_state
from material_ui._lab import DropShadow
from material_ui.shape import Shape
from material_ui.tokens import md_comp_menu as tokens

_CONTAINER_DROP_SHADOW_SPACE = 10
"""Extra space around the menu container to accommodate the drop shadow."""


class Menu(Component):
    """A popup menu that displays a list of selectable items."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Popup
            | Qt.WindowType.NoDropShadowWindowHint
            | Qt.WindowType.FramelessWindowHint,
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        container = Shape()
        container.color = tokens.container_color
        container.corner_shape = tokens.container_shape
        drop_shadow = DropShadow()
        drop_shadow.shadow_color = tokens.container_shadow_color
        drop_shadow.elevation = tokens.container_elevation
        drop_shadow.setParent(container)
        container.setGraphicsEffect(drop_shadow)
        # Margin to contain the drop shadow.
        drop_shadow_margin = QMargins(
            _CONTAINER_DROP_SHADOW_SPACE,
            _CONTAINER_DROP_SHADOW_SPACE,
            _CONTAINER_DROP_SHADOW_SPACE,
            _CONTAINER_DROP_SHADOW_SPACE,
        )
        self.overlay_widget(container, margins=drop_shadow_margin)

    def open(self, anchor_widget: Component) -> None:
        """Open the menu anchored to a specific widget.

        Args:
            anchor_widget: The widget to anchor the menu to.
        """
        pos = anchor_widget.mapToGlobal(QPoint(0, anchor_widget.height()))
        pos -= QPoint(0, _CONTAINER_DROP_SHADOW_SPACE)
        self.move(pos)
        self.resize(100, 100)
        self.show()


class MenuItem(Component):
    """A single menu item."""

    text = use_state("")
    """Text displayed in the menu item."""

    on_click: Signal
    """Emitted with the menu item is clicked."""

    def __init__(self) -> None:
        super().__init__()
