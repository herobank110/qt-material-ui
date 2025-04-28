from qtpy import QtCore, QtGui
from material_ui._component import Component, Signal, effect, use_state
from material_ui.shape import Shape

_UNSELECTED_TRACK_OUTLINE_COLOR = "#79747E"
_UNSELECTED_TRACK_COLOR = QtGui.QColor("#E6E0E9")
_UNSELECTED_HANDLE_COLOR = "#79747E"
_UNSELECTED_HOVER_HANDLE_COLOR = "#49454F"
_SELECTED_HANDLE_COLOR = "#FFFFFF"
_SELECTED_HOVER_HANDLE_COLOR = "#EADDFF"
_SELECTED_TRACK_COLOR = QtGui.QColor("#6750A4")
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

_TRACK_GEOMETRY = QtCore.QRect(
    _STATE_LAYER_MARGIN, _STATE_LAYER_MARGIN, _TRACK_WIDTH, _TRACK_HEIGHT
)
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
    - (_TRACK_HEIGHT - _SELECTED_HANDLE_WIDTH) / 2,
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

    # Create states for the animated properties. Can't be bothered
    # animating the rest - these seem like the most useful.
    _handle_geometry = use_state(_UNSELECTED_HANDLE_GEOMETRY)
    _track_color = use_state(_UNSELECTED_TRACK_COLOR)

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(_SWITCH_WIDTH, _SWITCH_HEIGHT)

        self._track = Shape()
        self._track.corner_shape.set("full")
        self._track.setGeometry(_TRACK_GEOMETRY)
        self._track.setParent(self)

        self._state_layer = Shape()
        self._state_layer.sx.set({"background-color": _STATE_LAYER_COLOR})
        self._state_layer.corner_shape.set("full")
        self._state_layer.visible.bind(self.hovered)
        self._state_layer.setParent(self)

        self._handle = Shape()
        self._handle.corner_shape.set("full")
        self._handle.setParent(self)
        # TODO: make geometry a property of shape? even though conflict with qt property?
        # self._handle.geometry.bind(self._handle_geometry)
        self._handle_geometry.changed.connect(self._handle.setGeometry)

        # Set the internal selected state but use the change_requested
        # signal as source of truth, so using it as a 'controlled' input
        # the parent component can hook into into to set its bound state.
        self.change_requested.connect(self.selected.set)

    @effect(_track_color)
    def _apply_track_color(self):
        self._track.sx.set(
            lambda prev: prev
            | {"background-color": "#%06x" % self._track_color.get().rgb()}
        )

    @effect(selected, pressed, hovered)
    def _refresh_shapes(self):
        self._track_color.animate_to(
            _SELECTED_TRACK_COLOR if self.selected.get() else _UNSELECTED_TRACK_COLOR,
            # Shorter than the handle geometry animation to draw more
            # attention to the handle.
            duration_ms=70,
            easing=QtCore.QEasingCurve.InOutCubic,
        )
        self._track.sx.set(
            lambda prev: prev
            | {
                "border": f"{_TRACK_OUTLINE_WIDTH}px solid {_UNSELECTED_TRACK_OUTLINE_COLOR}"
                if not self.selected.get()
                else "none",
            }
        )

        self._handle_geometry.animate_to(
            _SELECTED_PRESSED_HANDLE_GEOMETRY
            if self.selected.get() and self.pressed.get()
            else _UNSELECTED_PRESSED_HANDLE_GEOMETRY
            if self.pressed.get()
            else _SELECTED_HANDLE_GEOMETRY
            if self.selected.get()
            else _UNSELECTED_HANDLE_GEOMETRY,
            duration_ms=100,
            easing=QtCore.QEasingCurve.InOutCubic,
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
