"""Menu component.

A popup menu that opens at a specific location and displays a list of
selectable items.
"""

from qtpy.QtCore import QMargins, QPoint, Qt

from material_ui._component import Component, Signal, use_state
from material_ui._lab import DropShadow
from material_ui.shape import Shape
from material_ui.tokens import md_comp_menu as tokens


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
        # self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Main container
        # self.sx = {"background-color": "transparent"}
        # self.sx = {"background-color": "red"}

        container = Shape()
        container.color = tokens.container_color
        container.corner_shape = tokens.container_shape
        drop_shadow = DropShadow()
        drop_shadow.shadow_color = tokens.container_shadow_color
        drop_shadow.elevation = tokens.container_elevation
        drop_shadow.setParent(container)
        container.setGraphicsEffect(drop_shadow)
        # Margin to contain the drop shadow.
        self.overlay_widget(container, margins=QMargins(5, 5, 5, 5))

    # def nativeEvent(self, event_type: str, message: object) -> tuple[bool, object]:
    #     print(f"Native event: {event_type}, message: {message}")
    #     return super().nativeEvent(event_type, message)

    def open(self, anchor_widget: Component) -> None:
        """Open the menu anchored to a specific widget.

        Args:
            anchor_widget: The widget to anchor the menu to.
        """
        pos = anchor_widget.mapToGlobal(QPoint(0, anchor_widget.height())) - QPoint(
            0,
            5,
        )
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
