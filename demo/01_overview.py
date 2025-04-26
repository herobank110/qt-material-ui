"""Quick overview of some of the available components."""

from qtpy import QtWidgets
from material_ui import Button, Typography


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()
    window = QtWidgets.QWidget()
    window.setWindowTitle("qt-material-ui - demo - 01_overview.py")
    window.resize(300, 200)

    vbox = QtWidgets.QVBoxLayout(window)

    headline_label = Typography(
        text="Overview",
        typescale="display",
    )
    vbox.addWidget(headline_label)

    description_label = Typography(
        text="Material 3 component library for Qt Widgets",
        typescale="title",
    )
    vbox.addWidget(description_label)

    click_me_button = Button(
        text="Click me",
        variant="filled",
    )
    vbox.addWidget(click_me_button)

    window.setLayout(vbox)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
