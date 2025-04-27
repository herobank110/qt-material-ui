"""Internal widgets common functionality and helpers for Qt Widgets."""

from typing import Callable, Generic, TypeVarTuple, Unpack, get_args
from qtpy import QtCore, QtWidgets


_Ts = TypeVarTuple("_Ts")


class Signal(Generic[Unpack[_Ts]]):
    """Type safe Qt signal wrapper type.

    This is to be used for type hinting only on class variables for
    classes deriving from `Component`. The actual value will be
    converted to a `QtCore.Signal` object in the class initialization.
    """

    def connect(self, slot: Callable[[Unpack[_Ts]], None]) -> None: ...
    def disconnect(self, slot: Callable[[Unpack[_Ts]], None]) -> None: ...
    def emit(self, *args: Unpack[_Ts]) -> None: ...


class _ComponentMeta(type(QtCore.QObject)):
    """Meta class for all widgets."""

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        # Check if the class has a signal attribute
        for key, value in attrs.get("__annotations__", {}).items():
            if issubclass(getattr(value, "__origin__", None), Signal):
                # Convert the signal to a QtCore.Signal object
                num_args = len(get_args(value))
                if num_args == 0:
                    raise TypeError(
                        f"Signal {key} on class {name} must have at least one type argument"
                    )
                attrs[key] = QtCore.Signal(*["QVariant"] * num_args)

        # Create the class
        return super().__new__(cls, name, bases, attrs)


class Component(QtWidgets.QWidget, metaclass=_ComponentMeta):
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
