"""Base class for Text Field components."""

from material_ui import component
from material_ui._component import Signal, effect, use_state
from material_ui.tokens import md_comp_filled_text_field
from qtpy.QtWidgets import QLineEdit

from material_ui.typography import Typography


class BaseTextField(component.Component):
    """Base class for Text Field components."""

    label = use_state("Label")
    value = use_state("")

    changed = Signal[str]
    """Emitted when the value changed."""

    def __init__(self) -> None:
        super().__init__()

        self._label = Typography()
        self._label.text.bind(self.label)

        self._line_edit = QLineEdit()
        # self._line_edit.textEdited.connect(self._on_line_edit_text_edited)
        self._line_edit.textEdited.connect(self.changed)

    @effect(value)
    def _apply_value(self, value: str) -> None:
        """Apply the value to the line edit."""
        self._line_edit.setText(value)
        # TODO: ensure cursor position is handled well
        # self._line_edit.setCursorPosition(len(value))

    # def _on_line_edit_text_edited(self, text: str) -> None:
    #     """Called when the user entered something."""
    #     self.changed.emit(text)
