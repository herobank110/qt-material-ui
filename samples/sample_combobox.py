"""Sample of using the ComboBox."""

from material_ui.combobox import ComboBox
from qtpy.QtWidgets import QApplication


class SampleComboBox(ComboBox):
    def __init__(self):
        super().__init__()
        self.resize(300, 100)
        # Add more ComboBox setup here as needed


def main():
    app = QApplication([])
    window = SampleComboBox()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
