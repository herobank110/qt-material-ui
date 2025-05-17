"""Base class for Text Field components."""

from typing import Literal, cast
from material_ui._component import Signal, effect, use_state, Component
from material_ui.tokens import md_comp_filled_text_field as tokens
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import QSize, Qt, QPoint

from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography

LabelState = Literal["resting", "floating"]


class BaseTextField(Component):
    """Base class for Text Field components."""

    label = use_state("Label")
    value = use_state("")

    changed: Signal[str]
    """Emitted when the value changed."""

    def __init__(self) -> None:
        super().__init__()

        self._resting_label = Typography()
        self._resting_label.text.bind(self.label)
        self._resting_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self._floating_label = Typography()
        self._floating_label.text.bind(self.label)
        self._floating_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self._line_edit = QLineEdit()
        # Disable Qt's default context menu.
        self._line_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._line_edit.textEdited.connect(self.changed.emit)

    def sizeHint(self) -> QSize:
        return QSize(200, resolve_token(tokens.container_height))

    @effect(value)
    def _apply_value(self) -> None:
        self._line_edit.setText(self.value.get())
        # TODO: ensure cursor position is handled well

    _label_state = use_state(cast(LabelState, "resting"))

    @effect(value)
    def _update_label_state(self) -> None:
        # TODO: Also floating if focused
        self._label_state = "floating" if self.value.get() else "resting"

    _RESTING_LABEL_POS = QPoint()
    _FLOATING_LABEL_POS = QPoint()

    @effect(_label_state)
    def _animate_labels(self) -> None:
        # TODO: animate the positions and opacities
        match self._label_state.get():
            case "resting":
                self._resting_label.show()
                # Weird Qt behavior - if widget is initially hidden it
                # has zero size when it is later shown.
                self._resting_label.resize(self._resting_label.sizeHint())
                self._floating_label.hide()
            case "floating":
                self._resting_label.hide()
                self._floating_label.show()
