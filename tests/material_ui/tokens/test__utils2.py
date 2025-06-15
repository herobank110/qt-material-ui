"""Tests for material_ui.tokens._utils.py."""

import pytest
from pytest_mock import MockerFixture
from qtpy.QtGui import QColor

from material_ui.theming.theme_hook import ThemeHook
from material_ui.tokens import (
    md_comp_switch,
    md_ref_palette,
    md_sys_color,
    md_sys_elevation,
    md_sys_shape,
)
from material_ui.tokens._utils import (
    DesignToken,
    _is_indirection,
    _resolve_indirection,
    find_root_token,
    override_token,
    resolve_token,
    to_python_name,
)


def test_DesignToken_hash_basic_tests() -> None:
    assert hash(md_sys_color.primary) != hash(md_ref_palette.primary40)
    assert hash(md_ref_palette.primary40) == hash(md_ref_palette.primary40)
    assert hash(md_ref_palette.primary40) != hash(md_ref_palette.primary30)


def test_DesignToken_hash_root_tokens_match() -> None:
    # Check the hash matches after resolving the indirection.
    assert hash(md_sys_elevation.level1) != hash(md_comp_switch.handle_elevation)
    assert hash(md_sys_elevation.level1) == hash(
        find_root_token(md_comp_switch.handle_elevation),
    )
    # The main use case is for using tokens as keys in a dict.
    config = {md_sys_elevation.level1: "foo"}
    result = config[find_root_token(md_comp_switch.handle_elevation)]
    assert result == "foo"


def test_resolve_token_direct_value() -> None:
    assert resolve_token(md_ref_palette.primary40) == QColor("#6750a4")


def test_resolve_token_indirection_1_level() -> None:
    assert resolve_token(md_sys_color.primary) == QColor("#6750a4")


def test_resolve_token_indirection_2_levels() -> None:
    assert resolve_token(md_comp_switch.focus_indicator_thickness) == 3


def test_resolve_token_invalid_indirection() -> None:
    with pytest.raises(ValueError):
        resolve_token(DesignToken("invalid_name"))


def test__resolve_indirection_invalid_module() -> None:
    assert _resolve_indirection("invalid_name") is None


def test__resolve_indirection_valid_module_invalid_name() -> None:
    assert _resolve_indirection("md.sys.color.invalid_name") is None


def test_find_root_token_itself() -> None:
    assert find_root_token(md_ref_palette.error10) == md_ref_palette.error10


def test_find_root_token_indirection() -> None:
    assert find_root_token(md_comp_switch.handle_elevation) == md_sys_elevation.level1


def test__is_indirection_str_enum() -> None:
    # TODO: remove this and use properly typed DesignTokens instead of
    #   str for Indirections
    assert not _is_indirection(md_sys_shape.corner_full)


def test_to_python_name() -> None:
    result = to_python_name("md.comp.elevated-button.container-color")
    assert result == "md_comp_elevated_button_container_color"


def test_override_token_value_token(mocker: MockerFixture):
    stub = mocker.stub()
    ThemeHook.get().on_change.connect(stub)

    override_token(md_sys_color.background, QColor("#ff0000"))
    assert stub.call_count == 1
    assert resolve_token(md_sys_color.background) == QColor("#ff0000")


def test_override_token_indirection(mocker: MockerFixture):
    stub = mocker.stub()
    ThemeHook.get().on_change.connect(stub)

    assert resolve_token(md_comp_switch.handle_elevation) == 1

    override_token(md_sys_elevation.level1, 10)
    assert stub.call_count == 1
    assert resolve_token(md_comp_switch.handle_elevation) == 10
