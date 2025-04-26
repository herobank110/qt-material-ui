"""Internal widgets common functionality and helpers for Qt Widgets."""

from qtpy import QtWidgets


class Widget(QtWidgets.QWidget):
    """Base class for all widgets."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setObjectName(self.__class__.__name__)
