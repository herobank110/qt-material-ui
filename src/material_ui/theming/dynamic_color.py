"""Dynamic color integration with materialyoucolor library."""

from functools import partial

from materialyoucolor.dynamiccolor.dynamic_color import DynamicColor
from materialyoucolor.dynamiccolor.material_dynamic_colors import MaterialDynamicColors
from materialyoucolor.scheme.dynamic_scheme import DynamicScheme
from qtpy.QtGui import QColor

from material_ui.tokens import md_sys_color
from material_ui.tokens._utils import DesignToken, override_token


def apply_dynamic_color_scheme(scheme: DynamicScheme) -> None:
    """Apply the dynamic color scheme to the application."""
    fn = partial(_apply_scheme_to_token, source_scheme=scheme)

    fn(md_sys_color.error, MaterialDynamicColors.error)
    fn(md_sys_color.error_container, MaterialDynamicColors.errorContainer)
    fn(md_sys_color.inverse_on_surface, MaterialDynamicColors.inverseOnSurface)
    fn(md_sys_color.inverse_primary, MaterialDynamicColors.inversePrimary)
    fn(md_sys_color.inverse_surface, MaterialDynamicColors.inverseSurface)
    fn(md_sys_color.on_error, MaterialDynamicColors.onError)
    fn(md_sys_color.on_error_container, MaterialDynamicColors.onErrorContainer)
    fn(md_sys_color.on_primary, MaterialDynamicColors.onPrimary)
    fn(md_sys_color.on_primary_container, MaterialDynamicColors.onPrimaryContainer)
    fn(md_sys_color.on_secondary, MaterialDynamicColors.onSecondary)
    fn(md_sys_color.on_secondary_container, MaterialDynamicColors.onSecondaryContainer)
    fn(md_sys_color.on_surface, MaterialDynamicColors.onSurface)
    fn(md_sys_color.on_surface_variant, MaterialDynamicColors.onSurfaceVariant)
    fn(md_sys_color.on_tertiary, MaterialDynamicColors.onTertiary)
    fn(md_sys_color.on_tertiary_container, MaterialDynamicColors.onTertiaryContainer)
    fn(md_sys_color.outline, MaterialDynamicColors.outline)
    fn(md_sys_color.outline_variant, MaterialDynamicColors.outlineVariant)
    fn(md_sys_color.primary, MaterialDynamicColors.primary)
    fn(md_sys_color.primary_container, MaterialDynamicColors.primaryContainer)
    fn(md_sys_color.secondary, MaterialDynamicColors.secondary)
    fn(md_sys_color.secondary_container, MaterialDynamicColors.secondaryContainer)
    fn(md_sys_color.shadow, MaterialDynamicColors.shadow)
    fn(md_sys_color.surface, MaterialDynamicColors.surface)
    fn(md_sys_color.surface_bright, MaterialDynamicColors.surfaceBright)
    fn(md_sys_color.surface_dim, MaterialDynamicColors.surfaceDim)
    fn(md_sys_color.surface_container, MaterialDynamicColors.surfaceContainer)
    fn(md_sys_color.surface_container_high, MaterialDynamicColors.surfaceContainerHigh)
    fn(
        md_sys_color.surface_container_highest,
        MaterialDynamicColors.surfaceContainerHighest,
    )
    fn(md_sys_color.surface_container_low, MaterialDynamicColors.surfaceContainerLow)
    fn(
        md_sys_color.surface_container_lowest,
        MaterialDynamicColors.surfaceContainerLowest,
    )
    fn(md_sys_color.surface_tint, MaterialDynamicColors.surfaceTint)
    fn(md_sys_color.surface_variant, MaterialDynamicColors.surfaceVariant)
    fn(md_sys_color.tertiary, MaterialDynamicColors.tertiary)
    fn(md_sys_color.tertiary_container, MaterialDynamicColors.tertiaryContainer)
    fn(md_sys_color.background, MaterialDynamicColors.background)


def _apply_scheme_to_token(
    target_token: DesignToken,
    source_color: DynamicColor,
    source_scheme: DynamicScheme,
) -> None:
    """Apply the dynamic color scheme to a specific token."""
    argb = source_color.get_argb(source_scheme)
    qt_color = QColor(argb & 0x00FFFFFF)
    override_token(target_token, qt_color)
