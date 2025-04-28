from qtpy import QtCore, QtGui
from material_ui._component import Component, Signal, effect, use_state
from material_ui.shape import Shape

_UNSELECTED_TRACK_OUTLINE_COLOR = "#79747E"
_UNSELECTED_TRACK_COLOR = "#E6E0E9"
_UNSELECTED_HANDLE_COLOR = "#79747E"
_UNSELECTED_HOVER_HANDLE_COLOR = "#49454F"
_SELECTED_HANDLE_COLOR = "#FFFFFF"
_SELECTED_HOVER_HANDLE_COLOR = "#EADDFF"
_SELECTED_TRACK_COLOR = "#6750A4"
_STATE_LAYER_COLOR = "rgba(0, 0, 0, 40)"

_TRACK_WIDTH = 52
_TRACK_HEIGHT = 32
_STATE_LAYER_MARGIN = 4
_STATE_LAYER_SIZE = 40
_SWITCH_WIDTH = _TRACK_WIDTH + _STATE_LAYER_MARGIN * 2
_SWITCH_HEIGHT = _TRACK_HEIGHT + _STATE_LAYER_MARGIN * 2
_TRACK_OUTLINE_WIDTH = 2
_UNSELECTED_HANDLE_WIDTH = 16
_PRESSED_HANDLE_WIDTH = 28
_SELECTED_HANDLE_WIDTH = 24

_UNSELECTED_HANDLE_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN + (_TRACK_HEIGHT - _UNSELECTED_HANDLE_WIDTH) / 2,
    _STATE_LAYER_MARGIN + (_TRACK_HEIGHT - _UNSELECTED_HANDLE_WIDTH) / 2,
    _UNSELECTED_HANDLE_WIDTH,
    _UNSELECTED_HANDLE_WIDTH,
)
_UNSELECTED_PRESSED_HANDLE_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
)
_SELECTED_PRESSED_HANDLE_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN + _TRACK_WIDTH - _PRESSED_HANDLE_WIDTH - _TRACK_OUTLINE_WIDTH,
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
)
_SELECTED_HANDLE_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN
    + _TRACK_WIDTH
    - _SELECTED_HANDLE_WIDTH
    - _TRACK_OUTLINE_WIDTH * 2,
    _STATE_LAYER_MARGIN + (_TRACK_HEIGHT - _SELECTED_HANDLE_WIDTH) / 2,
    _SELECTED_HANDLE_WIDTH,
    _SELECTED_HANDLE_WIDTH,
)
_UNSELECTED_STATE_LAYER_GEOMETRY = QtCore.QRect(
    0,
    0,
    _STATE_LAYER_SIZE,
    _STATE_LAYER_SIZE,
)
_SELECTED_STATE_LAYER_GEOMETRY = QtCore.QRect(
    _SWITCH_WIDTH - _SWITCH_HEIGHT,
    0,
    _STATE_LAYER_SIZE,
    _STATE_LAYER_SIZE,
)


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

        self.setFixedSize(_SWITCH_WIDTH, _SWITCH_HEIGHT)

        self._state_layer = Shape()
        self._state_layer.setParent(self)
        self._state_layer.sx.set(
            {
                "background-color": _STATE_LAYER_COLOR,
                "border-radius": "20px",
            }
        )
        self._state_layer.setGeometry(_SELECTED_STATE_LAYER_GEOMETRY)
        self._state_layer.visible.bind(self.hovered)

        self._handle = Shape()
        self._handle.corner_shape.set("full")
        self._handle.setParent(self)

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
                "background-color": _UNSELECTED_TRACK_COLOR,
                "border": f"2px solid {_UNSELECTED_TRACK_OUTLINE_COLOR}",
            }
        else:
            # selected
            style = {
                "background-color": _SELECTED_TRACK_COLOR,
            }

        # TODO: find some way to use corner radius token full with resize event in the base class and merge it with the style dict
        style.update(
            {
                "border-radius": "16px",
                "margin": "4px",
            }
        )
        self.sx.set(style)

    @effect(selected, pressed, hovered)
    def _refresh_shapes(self):
        self._handle.setGeometry(
            _SELECTED_PRESSED_HANDLE_GEOMETRY
            if self.selected.get() and self.pressed.get()
            else _UNSELECTED_PRESSED_HANDLE_GEOMETRY
            if self.pressed.get()
            else _SELECTED_HANDLE_GEOMETRY
            if self.selected.get()
            else _UNSELECTED_HANDLE_GEOMETRY
        )
        self._handle.sx.set(
            lambda prev: prev
            | {
                "background-color": _SELECTED_HOVER_HANDLE_COLOR
                if self.selected.get() and self.hovered.get()
                else _SELECTED_HANDLE_COLOR
                if self.selected.get()
                else _UNSELECTED_HOVER_HANDLE_COLOR
                if self.hovered.get()
                else _UNSELECTED_HANDLE_COLOR
            }
        )

        self._state_layer.setGeometry(
            _SELECTED_STATE_LAYER_GEOMETRY
            if self.selected.get()
            else _UNSELECTED_STATE_LAYER_GEOMETRY
        )

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
