"""Tests for trailing icon functionality in text fields."""

from material_ui.icon import Icon
from material_ui.text_fields import FilledTextField, OutlinedTextField


def test_base_text_field_trailing_icon_property():
    """Test that BaseTextField has trailing_icon property."""
    filled = FilledTextField()
    outlined = OutlinedTextField()
    
    # Test initial state
    assert filled.trailing_icon is None
    assert outlined.trailing_icon is None
    
    # Create an icon
    search_icon = Icon()
    search_icon.icon_name = "search"
    
    # Test setting trailing icon
    filled.trailing_icon = search_icon
    outlined.trailing_icon = search_icon
    
    assert filled.trailing_icon is search_icon
    assert outlined.trailing_icon is search_icon
    
    # Test clearing trailing icon
    filled.trailing_icon = None
    outlined.trailing_icon = None
    
    assert filled.trailing_icon is None
    assert outlined.trailing_icon is None


def test_trailing_icon_wrapper_exists():
    """Test that _trailing_icon_wrapper is created in text fields."""
    filled = FilledTextField()
    outlined = OutlinedTextField()
    
    # Check that wrapper exists
    assert hasattr(filled, '_trailing_icon_wrapper')
    assert hasattr(outlined, '_trailing_icon_wrapper')
    
    # Check that wrapper is a Component
    from material_ui._component import Component
    assert isinstance(filled._trailing_icon_wrapper, Component)
    assert isinstance(outlined._trailing_icon_wrapper, Component)


def test_trailing_icon_placement():
    """Test that trailing icon is properly placed when set."""
    filled = FilledTextField()
    
    # Create and set an icon
    search_icon = Icon()
    search_icon.icon_name = "search"
    filled.trailing_icon = search_icon
    
    # Check that the icon was placed in the wrapper
    wrapper_children = filled._trailing_icon_wrapper.findChildren(Icon)
    assert len(wrapper_children) == 1
    assert wrapper_children[0] is search_icon
    
    # Test replacing the icon
    clear_icon = Icon()
    clear_icon.icon_name = "clear"
    filled.trailing_icon = clear_icon
    
    # Check that only the new icon is present
    wrapper_children = filled._trailing_icon_wrapper.findChildren(Icon)
    assert len(wrapper_children) == 1
    assert wrapper_children[0] is clear_icon
    
    # Test removing the icon
    filled.trailing_icon = None
    wrapper_children = filled._trailing_icon_wrapper.findChildren(Icon)
    assert len(wrapper_children) == 0