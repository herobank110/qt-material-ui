"""Menu component.

A popup menu that opens at a specific location and displays a list of
selectable items.
"""

from material_ui._component import Component, Signal, use_state


class Menu(Component):
    """A popup menu that displays a list of selectable items."""

    def __init__(self) -> None:
        super().__init__()


class MenuItem(Component):
    """A single menu item."""

    text = use_state("")
    """Text displayed in the menu item."""

    on_click: Signal
    """Emitted with the menu item is clicked."""

    def __init__(self) -> None:
        super().__init__()
