"""Internal widgets common functionality and helpers for Qt Widgets."""

from qtpy import QtWidgets


class Component(QtWidgets.QWidget):
    """Base class for all widgets."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def overlay_widget(self, widget: QtWidgets.QWidget) -> None:
        """Overlay a widget on top of this widget.

        Ownership will also be set to this widget.
        """
        widget.setParent(self)
        if self.layout() is not None:
            raise NotImplementedError("Multiple overlay widgets not supported yet")
        # TODO: add some other kind of 'overlay' layout similar to graphics anchors?
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
