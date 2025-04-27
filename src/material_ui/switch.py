from qtpy import QtWidgets
from material_ui._component import Component, Signal

md_comp_switch_unselected_track_outline_color = "#79747E"
md_comp_switch_unselected_track_color = "#E6E0E9"


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self, *, defaultChecked: bool = False) -> None:
        super().__init__()
        # self.checked = defaultChecked

        self.setFixedSize(52, 32)
        self.setStyleSheet(
            ";".join(
                map(
                    ":".join,
                    {
                        "background-color": md_comp_switch_unselected_track_color,
                        "border-radius": "16px",
                        "border": f"2px solid {md_comp_switch_unselected_track_outline_color}",
                    }.items(),
                )
            )
        )
