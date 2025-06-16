import pytest
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from qtpy.QtGui import QColor

from material_ui.theming.dynamic_color import apply_dynamic_color_scheme
from material_ui.tokens import md_sys_color
from material_ui.tokens._utils import resolve_token


# Mark it last as it modifies global state. May clean this up later.
@pytest.mark.order("last")
def test_apply_dynamic_color_scheme_basic():
    light_blue_scheme = SchemeTonalSpot(
        Hct.from_int(0xFF4181EE),
        is_dark=False,
        contrast_level=0.0,
    )
    apply_dynamic_color_scheme(light_blue_scheme)
    assert resolve_token(md_sys_color.primary) == QColor("#445e91")
    assert resolve_token(md_sys_color.surface) == QColor("#f9f9ff")

    dark_pink_scheme = SchemeTonalSpot(
        Hct.from_int(0xFFD224B5),
        is_dark=True,
        contrast_level=0.0,
    )
    apply_dynamic_color_scheme(dark_pink_scheme)
    assert resolve_token(md_sys_color.primary) == QColor("#f6b2df")
    assert resolve_token(md_sys_color.surface) == QColor("#181215")
