from qtpy import QtCore, QtGui, QtWidgets
from material_ui._component import Component, Signal, effect, use_state

md_comp_switch_unselected_track_outline_color = "#79747E"
md_comp_switch_unselected_track_color = "#E6E0E9"
md_comp_switch_selected_track_color = "#6750A4"
md_comp_switch_selected_handle_color = "#FFFFFF"
state_layer_color = "rgba(0, 0, 0, 40)"


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    selected = use_state(False)
    hovered = use_state(False)
    pressed = use_state(False)
    disabled = use_state(False)

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(52 + 8, 32 + 8)

        state_layer = Component()
        state_layer.setParent(self)
        state_layer.setStyleSheet(
            f"background:{state_layer_color};border-radius:20px;border:none;margin:0px;"
        )
        state_layer.setGeometry(QtCore.QRect(52 - (32 - 8) - 8, 0, 32 + 8, 32 + 8))
        state_layer.setVisible(self.hovered.get())  # initial state - TODO: use binding
        # For some reason this fn needs to be wrapped in a lambda.
        self.hovered.changed.connect(lambda value: state_layer.setVisible(value))
        # TODO: create a Shape class and have duplicate stuff like visible as Variable.
        # ripple.visible.bind(self.hovered)

        handle = Component(corner="full")
        handle.setParent(self)
        handle.setStyleSheet(
            f"background:{md_comp_switch_selected_handle_color};border:none;border-radius:14px;margin:0px;"
        )
        handle.setGeometry(QtCore.QRect(52 - 28 - 2 + 4, 2 + 4, 28, 28))

        # Set the internal selected state but use the change_requested
        # signal as source of truth, so using it as a 'controlled' input
        # the parent component can hook into into to set its bound state.
        self.change_requested.connect(self.selected.set)

    @effect(selected)
    def _apply_style(self) -> None:
        """Apply the style based on the selected state."""
        if not self.selected.get():
            # unselected
            style = {
                "background-color": md_comp_switch_unselected_track_color,
                "border": f"2px solid {md_comp_switch_unselected_track_outline_color}",
            }
        else:
            # selected
            style = {
                "background-color": md_comp_switch_selected_track_color,
            }

        # TODO: find some way to use corner radius token full with resize event in the base class and merge it with the style dict
        style.update(
            {
                "border-radius": "16px",
                "margin": "4px",
            }
        )
        self.sx.set(style)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if event.button() == QtCore.Qt.LeftButton:
            self.pressed.set(True)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        self.pressed.set(False)
        mouse_inside = self.rect().contains(event.pos())
        if event.button() == QtCore.Qt.LeftButton and mouse_inside:
            self.change_requested.emit(not self.selected.get())
        return super().mouseReleaseEvent(event)

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:  # noqa: N802
        self.hovered.set(True)
        return super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:  # noqa: N802
        self.hovered.set(False)
        return super().leaveEvent(event)
