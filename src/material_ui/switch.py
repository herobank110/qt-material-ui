from qtpy import QtCore, QtGui
from material_ui._component import Component, Signal, effect, use_state

md_comp_switch_unselected_track_outline_color = "#79747E"
md_comp_switch_unselected_track_color = "#E6E0E9"
md_comp_switch_selected_track_color = "#6750A4"
md_comp_switch_selected_handle_color = "#FFFFFF"


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    selected = use_state(False)

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(52, 32)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if event.button() == QtCore.Qt.LeftButton:
            # Toggle the checked state
            self.selected.set(not self.selected.get())
        return super().mousePressEvent(event)

    @effect(selected)
    def _apply_style(self) -> None:
        """Apply the style based on the selected state."""
        base = {
            "background-color": md_comp_switch_unselected_track_color,
            "border-radius": "16px",
            "border": f"2px solid {md_comp_switch_unselected_track_outline_color}",
        }
        if self.selected.get():
            base.update(
                {
                    "background-color": md_comp_switch_selected_track_color,
                    "border": "none",
                }
            )
        self.sx.set(base)