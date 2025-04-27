"""Internal widgets common functionality and helpers for Qt Widgets."""

from typing import Any, Callable, Generic, TypeVar, TypeVarTuple, Unpack, get_args
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


_T = TypeVar("_T")


class Variable(Generic[_T]):
    """Type safe property wrapper object.

    Creates a Qt property with a getter and setter and changed signal.

    Also used for one-way data binding and defined dependencies between
    variables.
    """

    changed: Signal[_T]

    def __init__(self, default_value: _T) -> None:
        self._value = default_value
        self._default_value = default_value

    def bind(self, other: "Variable[_T]") -> None:
        """Bind this variable to another variable."""
        self.changed.connect(other.set)

    def set(self, value: _T) -> None:
        """Set the value of the variable."""
        if self._value != value:
            self._value = value
            self.changed.emit(value)

    def get(self) -> _T:
        """Get the value of the variable."""
        return self._value


def _find_signal_annotations(attrs: dict[str, Any]) -> dict[str, int]:
    """Find all signal annotations in the class attributes.

    Args:
        attrs: Class attributes dictionary.

    Returns:
        Dictionary of signal name and number of arguments.
    """
    ret_val = {}
    for key, value in attrs.get("__annotations__", {}).items():
        value = getattr(value, "__origin__", value)
        if value and issubclass(value, Signal):
            num_args = len(get_args(value))
            ret_val[key] = num_args
    return ret_val


class _ComponentMeta(type(QtCore.QObject)):
    """Meta class for all widgets."""

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        # Convert Signal annotations to actual Qt Signal objects.
        # Use QVariant to avoid runtime type checking by Qt. Can't
        # remember exact examples but it can fail for certain types.
        attrs.update(
            {
                key: QtCore.Signal(*["QVariant"] * num_args)
                for key, num_args in _find_signal_annotations(attrs).items()
            }
        )
        return super().__new__(cls, name, bases, attrs)


class Component(QtWidgets.QWidget, metaclass=_ComponentMeta):
    """Base class for all widgets."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

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

    def add_state(self, default_value: _T) -> Variable[_T]:
        """Add a state to the component.

        Args:
            value: The value of the state.

        Returns:
            The variable object.
        """
        var = Variable(default_value)
        return var
