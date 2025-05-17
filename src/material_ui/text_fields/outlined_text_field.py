"""Outlined text field component."""

from material_ui.text_fields._base_text_field import BaseTextField


class OutlinedTextField(BaseTextField):
    """Outlined text field component."""

    def __init__(self) -> None:
        super().__init__()
        self._floating_label.setParent(self)
        self._resting_label.setParent(self)
        self._line_edit.setParent(self)
