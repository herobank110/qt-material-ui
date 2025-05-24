"""Typography module."""

from typing import Literal, cast

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel

from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_sys_color, md_sys_typescale
from material_ui.tokens._utils import DesignToken

TypographyVariant = Literal[
    "display-small",
    "display-medium",
    "display-large",
    "headline-small",
    "headline-medium",
    "headline-large",
    "title-small",
    "title-medium",
    "title-large",
    "body-small",
    "body-medium",
    "body-large",
    "label-small",
    "label-medium",
    "label-large",
]

_VARIANT_SETTINGS_MAPPING: dict[
    TypographyVariant,
    tuple[DesignToken, DesignToken, DesignToken],
] = {
    "display-small": (
        md_sys_typescale.display_small_font,
        md_sys_typescale.display_small_size,
        md_sys_typescale.display_small_weight,
    ),
    "display-medium": (
        md_sys_typescale.display_medium_font,
        md_sys_typescale.display_medium_size,
        md_sys_typescale.display_medium_weight,
    ),
    "display-large": (
        md_sys_typescale.display_large_font,
        md_sys_typescale.display_large_size,
        md_sys_typescale.display_large_weight,
    ),
    "headline-small": (
        md_sys_typescale.headline_small_font,
        md_sys_typescale.headline_small_size,
        md_sys_typescale.headline_small_weight,
    ),
    "headline-medium": (
        md_sys_typescale.headline_medium_font,
        md_sys_typescale.headline_medium_size,
        md_sys_typescale.headline_medium_weight,
    ),
    "headline-large": (
        md_sys_typescale.headline_large_font,
        md_sys_typescale.headline_large_size,
        md_sys_typescale.headline_large_weight,
    ),
    "title-small": (
        md_sys_typescale.headline_small_font,
        md_sys_typescale.headline_small_size,
        md_sys_typescale.headline_small_weight,
    ),
    "title-medium": (
        md_sys_typescale.title_medium_font,
        md_sys_typescale.title_medium_size,
        md_sys_typescale.title_medium_weight,
    ),
    "title-large": (
        md_sys_typescale.title_large_font,
        md_sys_typescale.title_large_size,
        md_sys_typescale.title_large_weight,
    ),
    "body-small": (
        md_sys_typescale.body_small_font,
        md_sys_typescale.body_small_size,
        md_sys_typescale.body_small_weight,
    ),
    "body-medium": (
        md_sys_typescale.body_medium_font,
        md_sys_typescale.body_medium_size,
        md_sys_typescale.body_medium_weight,
    ),
    "body-large": (
        md_sys_typescale.body_large_font,
        md_sys_typescale.body_large_size,
        md_sys_typescale.body_large_weight,
    ),
    "label-small": (
        md_sys_typescale.label_small_font,
        md_sys_typescale.label_small_size,
        md_sys_typescale.label_small_weight,
    ),
    "label-medium": (
        md_sys_typescale.label_medium_font,
        md_sys_typescale.label_medium_size,
        md_sys_typescale.label_medium_weight,
    ),
    "label-large": (
        md_sys_typescale.label_large_font,
        md_sys_typescale.label_large_size,
        md_sys_typescale.label_large_weight,
    ),
}


class Typography(Component):
    """Typography helps make writing legible and beautiful."""

    text = use_state("")
    color = use_state(md_sys_color.on_surface)
    variant = use_state(cast("TypographyVariant | None", None))
    font_family = use_state(md_sys_typescale.body_medium_font)
    font_size = use_state(md_sys_typescale.body_medium_size)
    font_weight = use_state(md_sys_typescale.body_medium_weight)
    alignment = use_state(cast("Qt.AlignmentFlag", Qt.AlignmentFlag()))  # type: ignore[call-arg]

    def __init__(self) -> None:
        super().__init__()

        self._label = QLabel()
        self.overlay_widget(self._label)

    @effect(alignment)
    def _apply_alignment(self) -> None:
        self._label.setAlignment(self.alignment)

    @effect(text)
    def _apply_text(self) -> None:
        self._label.setText(self.text)

    @effect(variant)
    def _apply_font_settings_from_variant(self) -> None:
        if not self.variant:
            return
        variant = self.variant if "-" in self.variant else f"{self.variant}-medium"
        font_family, font_size, font_weight = _VARIANT_SETTINGS_MAPPING[variant]
        self.font_family = font_family
        self.font_size = font_size
        self.font_weight = font_weight

    @effect(font_family, font_size, font_weight, color)
    def _apply_styles(self) -> None:
        self.sx = {
            "font-family": self.font_family,
            "font-size": f"{self.font_size}px",
            "font-weight": self.font_weight,
            "color": self.color,
        }
