"""Base progress."""

from material_ui._component import Component, use_state


class BaseProgress(Component):
    """Base class for progress indicators."""

    value: float = use_state(0.0)
    """Progress percentage, in range [0, 1]."""

    indeterminate: bool = use_state(False)
    """Whether the progress is indeterminate (looping animation)."""
