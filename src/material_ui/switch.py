"""Switch component."""

from qtpy.QtCore import QEasingCurve, QRect
from qtpy.QtGui import QColor

from material_ui._component import Component, Signal, effect, use_state
from material_ui.shape import Shape
from material_ui.tokens import md_comp_switch as tokens

_UNSELECTED_TRACK_OUTLINE_COLOR = "#79747E"
_UNSELECTED_TRACK_COLOR = QColor("#E6E0E9")

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

_TRACK_GEOMETRY = QRect(
    _STATE_LAYER_MARGIN, _STATE_LAYER_MARGIN, _TRACK_WIDTH, _TRACK_HEIGHT
)
_UNSELECTED_HANDLE_GEOMETRY = QRect(
    _STATE_LAYER_MARGIN + (_TRACK_HEIGHT - _UNSELECTED_HANDLE_WIDTH) // 2,
    _STATE_LAYER_MARGIN + (_TRACK_HEIGHT - _UNSELECTED_HANDLE_WIDTH) // 2,
    _UNSELECTED_HANDLE_WIDTH,
    _UNSELECTED_HANDLE_WIDTH,
)
_UNSELECTED_PRESSED_HANDLE_GEOMETRY = QRect(
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
)
_SELECTED_PRESSED_HANDLE_GEOMETRY = QRect(
    _STATE_LAYER_MARGIN + _TRACK_WIDTH - _PRESSED_HANDLE_WIDTH - _TRACK_OUTLINE_WIDTH,
    _STATE_LAYER_MARGIN + _TRACK_OUTLINE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
    _PRESSED_HANDLE_WIDTH,
)
_SELECTED_HANDLE_GEOMETRY = QRect(
    _STATE_LAYER_MARGIN
    + _TRACK_WIDTH
    - _SELECTED_HANDLE_WIDTH
    - (_TRACK_HEIGHT - _SELECTED_HANDLE_WIDTH) // 2,
    _STATE_LAYER_MARGIN + (_TRACK_HEIGHT - _SELECTED_HANDLE_WIDTH) // 2,
    _SELECTED_HANDLE_WIDTH,
    _SELECTED_HANDLE_WIDTH,
)
_UNSELECTED_STATE_LAYER_GEOMETRY = QRect(
    0,
    0,
    _STATE_LAYER_SIZE,
    _STATE_LAYER_SIZE,
)
_SELECTED_STATE_LAYER_GEOMETRY = QRect(
    _SWITCH_WIDTH - _SWITCH_HEIGHT,
    0,
    _STATE_LAYER_SIZE,
    _STATE_LAYER_SIZE,
)


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    selected = use_state(False)
    disabled = use_state(False)

    # Create states for the animated properties.
    _handle_geometry = use_state(
        _UNSELECTED_HANDLE_GEOMETRY,
        transition=100,
        easing=QEasingCurve.Type.InOutCubic,
    )
    _track_color = use_state(
        _UNSELECTED_TRACK_COLOR,
        # Shorter than the handle geometry animation to draw more
        # attention to the handle.
        transition=70,
        easing=QEasingCurve.Type.InOutCubic,
    )

    on_change: Signal[bool]
    """Emitted when the user toggles the switch."""

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(_SWITCH_WIDTH, _SWITCH_HEIGHT)
        self.clicked.connect(self._on_click)
        self.should_propagate_click = False

        self._track = Shape()
        self._track.corner_shape = tokens.track_shape
        self._track.setGeometry(_TRACK_GEOMETRY)
        self._track.setParent(self)

        self._state_layer = Shape()
        self._state_layer.color = tokens.unselected_focus_state_layer_color
        self._state_layer.opacity = tokens.unselected_focus_state_layer_opacity
        self._state_layer.corner_shape = tokens.state_layer_shape
        self._state_layer.visible = self.hovered
        self._state_layer.setParent(self)

        self._handle = Shape()
        self._handle.corner_shape = tokens.handle_shape
        self._handle.setParent(self)

    def _on_click(self) -> None:
        """Handle click events to toggle the switch."""
        new_value = not self.selected
        self.selected = new_value
        self.on_change.emit(new_value)

    @effect(_handle_geometry)
    def _apply_handle_geometry(self) -> None:
        # TODO: make geometry a property of shape? even though conflict with qt property?
        self._handle.setGeometry(self._handle_geometry)

    @effect(selected)
    def _apply_track_color(self) -> None:
        self._track.color = (
            tokens.selected_track_color
            if self.selected
            else tokens.unselected_track_color
        )

    @effect(selected, Component.hovered)
    def _apply_handle_color(self) -> None:
        self._handle.color = (
            tokens.selected_hover_handle_color
            if self.selected and self.hovered
            else tokens.selected_handle_color
            if self.selected
            else tokens.unselected_hover_handle_color
            if self.hovered
            else tokens.unselected_handle_color
        )

    @effect(selected, Component.pressed, Component.hovered)
    def _refresh_shapes(self) -> None:
        selected_border = (
            f"{_TRACK_OUTLINE_WIDTH}px solid {_UNSELECTED_TRACK_OUTLINE_COLOR}"
        )
        self._track.sx = {
            **self._track.sx,
            "border": selected_border if not self.selected else "none",
        }

        self._handle_geometry = (
            _SELECTED_PRESSED_HANDLE_GEOMETRY
            if self.selected and self.pressed
            else _UNSELECTED_PRESSED_HANDLE_GEOMETRY
            if self.pressed
            else _SELECTED_HANDLE_GEOMETRY
            if self.selected
            else _UNSELECTED_HANDLE_GEOMETRY
        )

        self._state_layer.setGeometry(
            _SELECTED_STATE_LAYER_GEOMETRY
            if self.selected
            else _UNSELECTED_STATE_LAYER_GEOMETRY,
        )
