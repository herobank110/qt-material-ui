"""Sample of the typography component."""

from material_ui._component import Component
from material_ui.layout_basics import Stack
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtWidgets import QApplication


class SampleTypography(Component):
    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.background}

        stack = Stack(gap=8)

        for variant in ["display", "headline", "title", "body", "label"]:
            typography = Typography()
            typography.variant = variant
            typography.text = variant.title()
            stack.add_widget(typography)

        self.overlay_widget(stack)


def main() -> None:
    app = QApplication()
    window = SampleTypography()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
