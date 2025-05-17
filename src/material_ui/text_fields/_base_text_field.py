"""Base class for Text Field components."""

from material_ui._component import Signal, effect, use_state, Component

# Use one of these for the common tokens.
from material_ui.tokens import md_comp_filled_text_field as tokens
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import QSize

from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography


class BaseTextField(Component):
    """Base class for Text Field components."""

    label = use_state("Label")
    value = use_state("")

    changed: Signal[str]
    """Emitted when the value changed."""

    def __init__(self) -> None:
        super().__init__()

        self.sx = {
            "background-color": tokens.container_color,
        }

        self._label = Typography()
        self._label.text.bind(self.label)

        self._line_edit = QLineEdit()
        # self._line_edit.textEdited.connect(self._on_line_edit_text_edited)
        self._line_edit.textEdited.connect(self.changed.emit)

    def sizeHint(self) -> QSize:
        return QSize(200, resolve_token(tokens.container_height))

    @effect(value)
    def _apply_value(self) -> None:
        """Apply the value to the line edit."""
        self._line_edit.setText(self.value.get())
        # TODO: ensure cursor position is handled well
        # self._line_edit.setCursorPosition(len(value))

    # def _on_line_edit_text_edited(self, text: str) -> None:
    #     """Called when the user entered something."""
    #     self.changed.emit(text)
