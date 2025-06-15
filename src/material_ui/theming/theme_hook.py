"""Hook for the theme to notify when tokens changed (colors, etc)."""

from material_ui.hook import Hook


class ThemeHook(Hook):
    """Theme provider."""

    def sex():
        return 1


ThemeHook.get().sex
