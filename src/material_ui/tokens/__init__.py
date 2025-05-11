"""Design Token system.

Hardcoded values are available for all tokens. They can also be
overridden with an exported theme from Material Theme Builder plugin for
Figma, or dynamically generated.
"""

from material_ui.tokens._utils import (
    DesignToken,  # noqa: F401
    resolve_token,  # noqa: F401
    override_token,  # noqa: F401
)
