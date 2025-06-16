"""Hooks are dependencies that can be used across components.

A example use case would be a settings hook to persist user preferences
or a shopping cart hook to manage the user's shopping cart. This unlocks
easy access to shared state across components without the need for
bubbling state up and down the component tree.

However hooks may not always be the first solution, as they can obscure
functionality through a layer of abstraction.
"""

from functools import cache
from typing import TYPE_CHECKING, cast

from qtpy.QtCore import QObject
from qtpy.QtCore import Signal as QtSignal  # pyright: ignore[reportPrivateImportUsage]
from typing_extensions import Self

if TYPE_CHECKING:
    from material_ui._component import Signal


class Hook(QObject):
    """Base class for hooks."""

    on_change = cast("Signal", QtSignal())
    """Signal emitted when the hook's internal state has changed."""

    @classmethod
    @cache
    def get(cls) -> Self:
        """Get the singleton instance."""
        return cls()
