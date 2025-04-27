from qtpy import QtCore, QtGui
from material_ui._component import Component, Signal

md_comp_switch_unselected_track_outline_color = "#79747E"
md_comp_switch_unselected_track_color = "#E6E0E9"
md_comp_switch_selected_track_color = "#6750A4"
md_comp_switch_selected_handle_color = "#FFFFFF"


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self, *, defaultChecked: bool = False) -> None:
        super().__init__()

        # self.selected = self.add_state(defaultChecked)
        # self.sx.bind(self._get_sx, [self.selected])

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

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if event.button() == QtCore.Qt.LeftButton:
            # Toggle the checked state
            self.setStyleSheet(
                ";".join(
                    map(
                        ":".join,
                        {
                            "background-color": md_comp_switch_selected_track_color,
                            "border-radius": "16px",
                            "border": "none",
                        }.items(),
                    )
                )
            )
        return super().mousePressEvent(event)
