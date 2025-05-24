"""Sample of the typography component."""

from material_ui._component import Component
from material_ui.layout_basics import Stack
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication


class SampleTypography(Component):
    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.background}

        stack = Stack(gap=5, margins=QMargins(40, 30, 40, 30))

        for variant in [
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
            "label-large-prominent",
            "label-medium",
            "label-medium-prominent",
            "label-small",
        ]:
            typography = Typography()
            typography.variant = variant
            typography.text = variant.replace("-", " ").title()
            stack.add_widget(typography)

        self.overlay_widget(stack)


def main() -> None:
    app = QApplication()
    window = SampleTypography()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
