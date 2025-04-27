from material_ui._component import Component, Signal


class Switch(Component):
    """Switches toggle the selection of an item on or off."""
    on_change: Signal

    def __init__(self, *, defaultChecked: bool = False) -> None:
        super().__init__()
        self.checked = defaultChecked

        self.on_change.connect(lambda checked=1: print("checked", checked))
        self.on_change.emit()

