"""Typography module."""

from typing import TYPE_CHECKING, Literal, cast

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel

from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_sys_color, md_sys_typescale
from material_ui.tokens._utils import DesignToken, resolve_token, resolve_token_or_value

if TYPE_CHECKING:
    from qtpy.QtGui import QColor

TypographyVariant = Literal[
    "display-large",
    "display-medium",
    "headline-large",
    "headline-medium",
    "headline-small",
    "title-large",
    "title-medium",
    "title-small",
    "body-large",
    "body-medium",
    "body-small",
    "label-large",
    "label-medium",
    "label-small",
]

_VARIANT_SETTINGS_MAPPING: dict[
    TypographyVariant,
    tuple[DesignToken, DesignToken, DesignToken],
] = {
    "display-large": (
        md_sys_typescale.display_large_font,
        md_sys_typescale.display_large_size,
        md_sys_typescale.display_large_weight,
    ),
    "display-medium": (
        md_sys_typescale.display_medium_font,
        md_sys_typescale.display_medium_size,
        md_sys_typescale.display_medium_weight,
    ),
    "headline-large": (
        md_sys_typescale.headline_large_font,
        md_sys_typescale.headline_large_size,
        md_sys_typescale.headline_large_weight,
    ),
    "headline-medium": (
        md_sys_typescale.headline_medium_font,
        md_sys_typescale.headline_medium_size,
        md_sys_typescale.headline_medium_weight,
    ),
    "headline-small": (
        md_sys_typescale.headline_small_font,
        md_sys_typescale.headline_small_size,
        md_sys_typescale.headline_small_weight,
    ),
    "title-large": (
        md_sys_typescale.title_large_font,
        md_sys_typescale.title_large_size,
        md_sys_typescale.title_large_weight,
    ),
    "title-medium": (
        md_sys_typescale.title_medium_font,
        md_sys_typescale.title_medium_size,
        md_sys_typescale.title_medium_weight,
    ),
    "title-small": (
        md_sys_typescale.title_small_font,
        md_sys_typescale.title_small_size,
        md_sys_typescale.title_small_weight,
    ),
    "body-large": (
        md_sys_typescale.body_large_font,
        md_sys_typescale.body_large_size,
        md_sys_typescale.body_large_weight,
    ),
    "body-medium": (
        md_sys_typescale.body_medium_font,
        md_sys_typescale.body_medium_size,
        md_sys_typescale.body_medium_weight,
    ),
    "body-small": (
        md_sys_typescale.body_small_font,
        md_sys_typescale.body_small_size,
        md_sys_typescale.body_small_weight,
    ),
    "label-large": (
        md_sys_typescale.label_large_font,
        md_sys_typescale.label_large_size,
        md_sys_typescale.label_large_weight,
    ),
    "label-medium": (
        md_sys_typescale.label_medium_font,
        md_sys_typescale.label_medium_size,
        md_sys_typescale.label_medium_weight,
    ),
    "label-small": (
        md_sys_typescale.label_small_font,
        md_sys_typescale.label_small_size,
        md_sys_typescale.label_small_weight,
    ),
}


class Typography(Component):
    """Typography helps make writing legible and beautiful."""

    text = use_state("")
    color = use_state(cast("DesignToken | QColor", md_sys_color.on_surface))
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
        font_family, font_size, font_weight = _VARIANT_SETTINGS_MAPPING[self.variant]
        self.font_family = font_family
        self.font_size = font_size
        self.font_weight = font_weight

    @effect(font_family, font_size, font_weight, color)
    def _apply_styles(self) -> None:
        self.sx = {
            "font-family": cast("str", resolve_token(self.font_family)),
            "font-size": f"{resolve_token(self.font_size)}px",
            "font-weight": cast("str", resolve_token(self.font_weight)),
            "color": resolve_token_or_value(self.color),
        }
