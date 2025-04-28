"""Basic shape utility widget."""

from material_ui._component import Component, use_state


class Shape(Component):
    """A blank component with common shape features."""

    visible = use_state(True)

    def __init__(self) -> None:
        super().__init__()

        self.visible.changed.connect(lambda value: self.setVisible(value))
