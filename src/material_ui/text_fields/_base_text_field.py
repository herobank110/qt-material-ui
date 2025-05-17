"""Base class for Text Field components."""

from material_ui._component import Signal, effect, use_state, Component
from material_ui.layout_basics import Row
from material_ui.shape import Shape
from material_ui.tokens import md_comp_filled_text_field as tokens
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import QSize, QMargins, Qt

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

        row = Row()
        row.gap = 16
        row.margins = QMargins(16, 8, 16, 8)
        self.overlay_widget(row)

        self._label = Typography()
        self._label.text.bind(self.label)
        self._label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._label.setParent(self)

        # Use a wrapper to use the sx property, which Qt will propagate
        # to children by default.
        line_edit_wrapper = Component()
        line_edit_wrapper.sx = {
            "color": tokens.input_text_color,
            "font-family": tokens.input_text_font,
            "font-size": tokens.input_text_size,
            "font-weight": tokens.input_text_weight,
        }
        self._line_edit = QLineEdit()
        # Disable Qt's default context menu as style is different.
        self._line_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self._line_edit.textEdited.connect(self.changed.emit)
        # self._line_edit.setFont()
        line_edit_wrapper.overlay_widget(self._line_edit)
        row.add_widget(line_edit_wrapper)

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
