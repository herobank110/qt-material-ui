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

    label = use_state("Label")
    value = use_state("")

    changed: Signal[str]
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

    def sizeHint(self) -> QSize:  # noqa: N802
        height = resolve_token(tokens.container_height)
        if not isinstance(height, int):
            raise TypeError
        return QSize(200, height)

    def _on_clicked(self) -> None:
        # Focus the itself when clicked.
        self.setFocus(Qt.FocusReason.MouseFocusReason)
        # Select all text in the line edit.
        self._line_edit.setSelection(0, len(self.value))

    def _on_line_edit_text_edited(self, text: str) -> None:
        # Set the internal value already for non-controlled text fields.
        # However the controlled case would also set it again.
        self.value = text
        self.changed.emit(text)

    @effect(value)
    def _apply_value(self) -> None:
        self._line_edit.setText(self.value)
        # TODO: ensure cursor position is handled well

    _label_state = use_state(cast("LabelState", "resting"))

    @effect(value, Component.focused)
    def _update_label_state(self) -> None:
        self._label_state = "floating" if self.value or self.focused else "resting"

    _RESTING_LABEL_POS = QPoint()
    _FLOATING_LABEL_POS = QPoint()

    @effect(_label_state)
    def _animate_labels(self) -> None:
        # TODO: animate the positions and opacities
        match self._label_state:
            case "resting":
                self._resting_label.show()
                # Weird Qt behavior - if widget is initially hidden it
                # has zero size when it is later shown.
                self._resting_label.resize(self._resting_label.sizeHint())
                self._floating_label.hide()
            case "floating":
                self._resting_label.hide()
                self._floating_label.show()
            case _:
                raise ValueError
