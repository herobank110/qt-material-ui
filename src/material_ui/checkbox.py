"""Checkbox component."""

from qtpy.QtGui import QColor, QImage, QLinearGradient, QPainter
from qtpy.QtWidgets import QGraphicsOpacityEffect

from material_ui._component import Component, effect, use_state
from material_ui.icon import Icon
from material_ui.shape import Shape
from material_ui.tokens import md_comp_checkbox as tokens
from material_ui.tokens._utils import resolve_token


class Checkbox(Component):
    """Checkbox component."""

    selected = use_state(False)
    """Whether the checkbox is checked."""

    indeterminate = use_state(False)
    """Whether the checkbox is in an indeterminate state."""

    _icon_name = use_state("check")

    def __init__(self) -> None:
        super().__init__()

        container = Shape()
        container.corner_shape = tokens.container_shape
        container.setFixedSize(
            resolve_token(tokens.container_height),
            resolve_token(tokens.container_width),
        )
        container.color = resolve_token(tokens.selected_container_color)
        self.overlay_widget(container)

        icon = Icon()
        icon.icon_name = self._icon_name
        icon.font_size = tokens.icon_size
        icon.color = tokens.selected_icon_color

        icon_opacity_effect = QGraphicsOpacityEffect()
        icon_opacity_effect.setOpacity(1.0)
        icon_opacity_effect.setParent(icon)

        # mask = QImage(18, 18, QImage.Format.Format_ARGB32_Premultiplied)
        # painter = QPainter(mask)
        # painter.setRenderHints(QPainter.RenderHint.Antialiasing, on=False)
        # painter.fillRect(0, 0, 18, 18, "transparent")
        # # painter.fillRect(0, 0, 9, 18, "white")
        # painter.end()
        # icon_opacity_effect.setOpacityMask(mask)

        grad = QLinearGradient()
        grad.setStart(0, 0)
        grad.setFinalStop(18, 0)
        grad.setColorAt(0.5, "black")
        grad.setColorAt(1, "transparent")
        icon_opacity_effect.setOpacityMask(grad)

        icon.setGraphicsEffect(icon_opacity_effect)
        icon.update()

        container.overlay_widget(icon)

        self.clicked.connect(self._on_clicked)
        self.should_propagate_click = False

    def _on_clicked(self) -> None:
        if self.indeterminate:
            self.indeterminate = False
            self.selected = True
        else:
            self.selected = not self.selected

    @effect(selected, indeterminate)
    def _apply_icon(self) -> None:
        if self.indeterminate:
            self._icon_name = "check_indeterminate_small"
        elif self.selected:
            self._icon_name = "check"
        else:
            self._icon_name = ""
