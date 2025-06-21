"""Menu component.

A popup menu that opens at a specific location and displays a list of selectable items.
"""

from typing import cast

from qtpy.QtCore import QEvent, QPoint, Qt
from qtpy.QtGui import QEnterEvent, QFocusEvent, QKeyEvent, QMouseEvent, QShowEvent
from qtpy.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

from material_ui._component import Component, Signal, effect, use_state
from material_ui.icon import Icon
from material_ui.shape import Shape
from material_ui.tokens import md_comp_menu as tokens
from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography


class MenuItem(Component):
    """A single menu item with optional icon."""

    clicked: Signal
    """Emitted when the menu item is clicked."""

    text = use_state("")
    """Text displayed in the menu item."""

    icon_name = use_state("")
    """Name of the material icon to display next to the text. Empty means no icon."""

    selected = use_state(False)
    """Whether this item is currently selected."""

    _hovered = use_state(False)
    _pressed = use_state(False)

    def __init__(self) -> None:
        super().__init__()

        self.clicked.connect(self._on_clicked)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Container layout
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Item content
        self._content = QWidget()
        container_layout.addWidget(self._content)

        # Content layout with padding
        content_layout = QHBoxLayout(self._content)
        content_layout.setContentsMargins(16, 0, 16, 0)
        content_layout.setSpacing(12)

        # Icon (if provided)
        self._icon = Icon()
        self._icon.icon_name = self.icon_name
        self._icon.font_size = tokens.list_item_with_leading_icon_leading_icon_size
        content_layout.addWidget(self._icon)

        # Text label
        self._label = Typography()
        self._label.text = self.text
        self._label.alignment = Qt.AlignmentFlag.AlignVCenter
        content_layout.addWidget(self._label)

        # State layer for hover/press effects
        self._state_layer = Shape()
        self._state_layer.setParent(self)
        self._state_layer.corner_shape = tokens.container_shape

        self.setFixedHeight(
            cast("int", resolve_token(tokens.list_item_container_height)),
        )
        self._update_styles()

    def _on_clicked(self) -> None:
        pass  # This will be connected to by the Menu component

    @effect(selected, _hovered, _pressed)
    def _update_styles(self) -> None:
        """Update styles based on current state."""
        self._state_layer.resize(self.size())

        # Base styles
        state_layer_opacity = 0.0
        text_color = tokens.list_item_label_text_color

        # Selected state takes precedence
        if self.selected:
            self._content.setStyleSheet(f"""
                background-color: {resolve_token(tokens.list_item_selected_container_color)};
            """)
            text_color = tokens.list_item_selected_label_text_color
            if self.icon_name:
                self._icon.color = (
                    tokens.list_item_selected_with_leading_icon_leading_icon_color
                )
        else:
            self._content.setStyleSheet("")
            if self.icon_name:
                self._icon.color = tokens.list_item_with_leading_icon_leading_icon_color

            # Apply hover/press state
            if self._pressed:
                state_layer_opacity = tokens.list_item_pressed_state_layer_opacity
                text_color = tokens.list_item_pressed_label_text_color
                if self.icon_name:
                    self._icon.color = (
                        tokens.list_item_with_leading_icon_pressed_icon_color
                    )
            elif self._hovered:
                state_layer_opacity = tokens.list_item_hover_state_layer_opacity
                text_color = tokens.list_item_hover_label_text_color
                if self.icon_name:
                    self._icon.color = (
                        tokens.list_item_with_leading_icon_hover_icon_color
                    )

        # Apply text color
        self._label.sx = {
            "color": resolve_token(text_color),
            "font": resolve_token(tokens.list_item_label_text_font),
            "font-size": f"{resolve_token(tokens.list_item_label_text_size)}px",
            "font-weight": resolve_token(tokens.list_item_label_text_weight),
            "line-height": f"{resolve_token(tokens.list_item_label_text_line_height)}px",
        }

        # Apply state layer opacity
        self._state_layer.sx = {
            "background-color": resolve_token(tokens.list_item_hover_state_layer_color),
            "opacity": state_layer_opacity,
        }

    @effect(icon_name)
    def _update_icon(self) -> None:
        """Update icon visibility and name."""
        self._icon.icon_name = self.icon_name
        self._icon.setVisible(bool(self.icon_name))
        self._update_styles()

    def enterEvent(self, event: QEnterEvent) -> None:  # noqa: N802
        """Handle mouse enter event."""
        self._hovered = True
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:  # noqa: N802
        """Handle mouse leave event."""
        self._hovered = False
        self._pressed = False
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Handle mouse press event."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Handle mouse release event."""
        was_pressed = self._pressed
        self._pressed = False
        if event.button() == Qt.MouseButton.LeftButton and was_pressed:
            self.clicked.emit()
        super().mouseReleaseEvent(event)


class Menu(Component):
    """A popup menu that displays a list of selectable items."""

    items = use_state(cast("list[str]", []))
    """List of menu item texts to show."""

    item_icons = use_state(cast("list[str]", []))
    """List of icon names for each item. Empty strings mean no icon for that item."""

    selected_index = use_state(-1)
    """The currently selected item index, or -1 if nothing is selected."""

    on_selection_change: Signal[int]
    """Emitted when a menu item is selected. Provides the new selected index."""
    _position = use_state(QPoint(0, 0))
    _visible = use_state(False)
    _menu_items = use_state(cast("list[MenuItem]", []))

    def __init__(self) -> None:
        super().__init__()

        # Set up widget properties
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # Main container
        self._container = Shape()
        self._container.corner_shape = tokens.container_shape
        self._container.color = tokens.container_color

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._container)

        # Scroll area for menu items
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff,
        )
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self._container_layout = QVBoxLayout(self._container)
        self._container_layout.setContentsMargins(0, 0, 0, 0)
        self._container_layout.setSpacing(0)
        self._container_layout.addWidget(self._scroll_area)

        # Content widget inside scroll area
        self._content = QWidget()
        self._scroll_area.setWidget(self._content)
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)

        # Add any additional styles needed for the container
        self._container.opacity = 1.0

    @effect(_visible)
    def _update_visibility(self) -> None:
        """Update visibility based on the _visible state."""
        if self._visible:
            self.show()
            self.setFocus()
            self.activateWindow()
        else:
            self.hide()

    @effect(items, item_icons, selected_index)
    def _update_menu_items(self) -> None:
        """Update the menu items based on current configuration."""
        # Clear existing items
        for item in self._menu_items:
            self._content_layout.removeWidget(item)
            item.deleteLater()

        self._menu_items = []

        # Add new items
        for i, text in enumerate(self.items):
            item = MenuItem()
            item.text = text

            # Set icon if available
            if i < len(self.item_icons):
                item.icon_name = self.item_icons[i]

            # Set selected state
            item.selected = i == self.selected_index

            # Connect click handler
            item.clicked.connect(lambda idx=i: self._on_item_clicked(idx))

            # Add to layout
            self._content_layout.addWidget(item)
            self._menu_items.append(item)

        # Update size
        self._update_size()

    def _update_size(self) -> None:
        """Update the menu size based on content."""
        width = 200  # Default minimum width
        height = 0

        # Calculate required size based on items
        if self._menu_items:
            # Get the width hint from the widest item
            for item in self._menu_items:
                width = max(width, item.sizeHint().width())

            # Calculate height (limited to show max ~6 items without scrolling)
            item_height = cast("int", resolve_token(tokens.list_item_container_height))
            height = min(len(self._menu_items) * item_height, 6 * item_height)

        self.resize(width, height)

    def _on_item_clicked(self, index: int) -> None:
        """Handle menu item click."""
        self.selected_index = index
        self.on_selection_change.emit(index)
        self.hide()
        self._visible = False

    def showEvent(self, event: QShowEvent) -> None:  # noqa: N802
        """Handle show event."""
        # Position the menu at the specified point
        self.move(self._position)
        super().showEvent(event)

    def show_at(self, position: QPoint) -> None:
        """Show the menu at the specified position."""
        self._position = position
        self._visible = True

    def focusOutEvent(self, event: QFocusEvent) -> None:  # noqa: N802
        """Hide the menu when focus is lost."""
        self._visible = False
        super().focusOutEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        """Handle keyboard navigation."""
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self._visible = False
        elif key == Qt.Key.Key_Up:
            # Select previous item
            if self.selected_index > 0:
                self.selected_index -= 1
            elif self.items:  # Wrap around
                self.selected_index = len(self.items) - 1
        elif key == Qt.Key.Key_Down:
            # Select next item
            if self.selected_index < len(self.items) - 1:
                self.selected_index += 1
            elif self.items:  # Wrap around
                self.selected_index = 0
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # Activate selected item
            if 0 <= self.selected_index < len(self.items):
                self.on_selection_change.emit(self.selected_index)
                self._visible = False
        else:
            super().keyPressEvent(event)
