"""Base class for Text Field components."""

from typing import Literal, cast

from qtpy.QtCore import QPoint, QSize, Qt
from qtpy.QtWidgets import QLineEdit, QSizePolicy

from material_ui._component import Component, Signal, effect, use_state
from material_ui.tokens import md_comp_filled_text_field as tokens
from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography

LabelState = Literal["resting", "floating"]


class BaseTextField(Component):
    """Base class for Text Field components."""

    label = use_state("")
    """Floating label text."""

    value = use_state("")
    """Current value of the text field."""

    on_change: Signal[str]
    """Emitted when the value changed."""

    def __init__(self) -> None:
        super().__init__()

        self.setCursor(Qt.CursorShape.IBeamCursor)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self._resting_label = Typography()
        self._resting_label.text = self.label
        self._resting_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
        )

        self._floating_label = Typography()
        self._floating_label.text = self.label
        self._floating_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
        )

        self._line_edit = QLineEdit()
        # Disable Qt's default context menu.
        self._line_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._line_edit.textEdited.connect(self._on_line_edit_text_edited)
        # Focus pass through to the line edit.
        self.setFocusProxy(self._line_edit)

        self.clicked.connect(self._on_clicked)
        self.should_propagate_click = False

    _TOP_SPACE = 6

    def sizeHint(self) -> QSize:  # noqa: N802
        height = cast("int", resolve_token(tokens.container_height))
        return QSize(200, height + self._TOP_SPACE)

    def _on_clicked(self) -> None:
        # Focus the itself when clicked.
        self.setFocus(Qt.FocusReason.MouseFocusReason)
        # Select all text in the line edit.
        self._line_edit.setSelection(0, len(self.value))

    def _on_line_edit_text_edited(self, text: str) -> None:
        # Set the internal value already for non-controlled text fields.
        # However the controlled case would also set it again.
        self.value = text
        self.on_change.emit(text)

    @effect(value)
    def _apply_value(self) -> None:
        cursor_pos = self._line_edit.cursorPosition()
        self._line_edit.setText(self.value)
        # Ensure cursor position is maintained.
        self._line_edit.setCursorPosition(cursor_pos)

    _label_state = use_state(cast("LabelState", "resting"))

    @effect(value, Component.focused)
    def _update_label_state(self) -> None:
        self._label_state = "floating" if self.value or self.focused else "resting"

    # Configured in derived classes.
    _RESTING_LABEL_POS = QPoint()
    _FLOATING_LABEL_POS = QPoint()

    _resting_label_opacity = use_state(0.0, transition=80)
    _floating_label_opacity = use_state(0.0, transition=80)
    _resting_label_pos = use_state(QPoint(), transition=80)
    _floating_label_pos = use_state(QPoint(), transition=80)

    @effect(_label_state)
    def _animate_labels(self) -> None:
        # Animate the positions and opacities. Instead of animating font
        # size, animate the opacity and positions to make two labels
        # look like one.
        match self._label_state:
            case "resting":
                self._resting_label_opacity = 1.0
                self._floating_label_opacity = 0.0
                self._resting_label_pos = self._RESTING_LABEL_POS
                self._floating_label_pos = self._RESTING_LABEL_POS
            case "floating":
                self._resting_label_opacity = 0.0
                self._floating_label_opacity = 1.0
                self._resting_label_pos = self._FLOATING_LABEL_POS
                self._floating_label_pos = self._FLOATING_LABEL_POS

    @effect(_resting_label_opacity)
    def _apply_resting_label_opacity(self) -> None:
        self._resting_label.sx = {
            **self._resting_label.sx,
            "opacity": self._resting_label_opacity,
        }

    @effect(_floating_label_opacity)
    def _apply_floating_label_opacity(self) -> None:
        self._floating_label.sx = {
            **self._floating_label.sx,
            "opacity": self._floating_label_opacity,
        }

    @effect(_resting_label_pos)
    def _apply_resting_label_pos(self) -> None:
        self._resting_label.move(self._resting_label_pos)

    @effect(_floating_label_pos)
    def _apply_floating_label_pos(self) -> None:
        self._floating_label.move(self._floating_label_pos)
