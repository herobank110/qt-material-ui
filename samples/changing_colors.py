"""Sample of changing colors with design tokens theming system."""

from material_ui._component import Component
from qtpy.QtWidgets import QApplication


class ChangingColors(Component):
    def __init__(self) -> None:
        super().__init__()


# Color in hue, chroma, tone form
from materialyoucolor.hct import Hct

# There are 9 different variants of scheme.
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot

# Others you can import: SchemeExpressive, SchemeFruitSalad, SchemeMonochrome, SchemeRainbow, SchemeVibrant, SchemeNeutral, SchemeFidelity and SchemeContent

# SchemeTonalSpot is android default
scheme = SchemeTonalSpot(
    Hct.from_int(0xFF4181EE),
    is_dark=False,
    contrast_level=0.0,
)


def main() -> None:
    app = QApplication()
    window = ChangingColors()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
