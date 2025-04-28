from qtpy import QtCore, QtGui
from material_ui._component import Component, Signal, effect, use_state
from material_ui.shape import Shape

md_comp_switch_unselected_track_outline_color = "#79747E"
md_comp_switch_unselected_track_color = "#E6E0E9"
md_comp_switch_selected_track_color = "#6750A4"
md_comp_switch_selected_handle_color = "#FFFFFF"
state_layer_color = "rgba(0, 0, 0, 40)"

_STATE_LAYER_MARGIN = 4
_TRACK_WIDTH = 52
_TRACK_HEIGHT = 32
_SWITCH_WIDTH = _TRACK_WIDTH + _STATE_LAYER_MARGIN * 2
_SWITCH_HEIGHT = _TRACK_HEIGHT + _STATE_LAYER_MARGIN * 2
_TRACK_OUTLINE_WIDTH = 2
_HANDLE_UNSELECTED_WIDTH = 16
_HANDLE_PRESSED_WIDTH = 28
_HANDLE_SELECTED_WIDTH = 24
_HANDLE_UNSELECTED_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN + _TRACK_HEIGHT - _HANDLE_UNSELECTED_WIDTH / 2,
    _STATE_LAYER_MARGIN + _TRACK_HEIGHT - _HANDLE_UNSELECTED_WIDTH / 2,
    _HANDLE_UNSELECTED_WIDTH,
    _HANDLE_UNSELECTED_WIDTH,
)
_HANDLE_PRESSED_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN + _TRACK_WIDTH - _HANDLE_PRESSED_WIDTH - _TRACK_OUTLINE_WIDTH,
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _HANDLE_PRESSED_WIDTH,
    _HANDLE_PRESSED_WIDTH,
)
_HANDLE_SELECTED_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN + _TRACK_WIDTH - _HANDLE_SELECTED_WIDTH - _TRACK_OUTLINE_WIDTH,
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _HANDLE_SELECTED_WIDTH,
    _HANDLE_SELECTED_WIDTH,
)


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    selected = use_state(False)
    hovered = use_state(False)
    pressed = use_state(False)
    disabled = use_state(False)
    _handle_geometry = use_state(_HANDLE_UNSELECTED_GEOMETRY)

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(_SWITCH_WIDTH, _SWITCH_HEIGHT)

        self._state_layer = Shape()
        self._state_layer.setParent(self)
        self._state_layer.sx.set(
            {
                "background-color": state_layer_color,
                "border-radius": "20px",
            }
        )
        self._state_layer.setGeometry(QtCore.QRect(52 - (32 - 8) - 8, 0, 32 + 8, 32 + 8))
        self._state_layer.setVisible(self.hovered.get())  # initial state - TODO: use binding
        # For some reason this fn needs to be wrapped in a lambda.
        # self.hovered.changed.connect(lambda value: self._state_layer.setVisible(value))
        # TODO: create a Shape class and have duplicate stuff like visible as Variable.
        self._state_layer.visible.bind(self.hovered)

        self._handle = Shape()
        self._handle.setParent(self)
        self._handle.sx.set(
            {
                "background-color": md_comp_switch_selected_handle_color,
                "border-radius": "14px",
            }
        )

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
