"""Internal widgets common functionality and helpers for Qt Widgets."""

from dataclasses import dataclass
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


class Variable(QtCore.QObject, Generic[_T]):
    """Type safe property wrapper object.

    Creates a Qt property with a getter and setter and changed signal.

    Also used for one-way data binding and defined dependencies between
    variables.
    """

    changed: Signal[_T] = QtCore.Signal("QVariant")

    def __init__(self, default_value: _T, name: str, component_name: str) -> None:
        super().__init__()
        self.setObjectName(name)
        self.__component_name = component_name
        self._value = default_value
        self._default_value = default_value

    def get(self) -> _T:
        """Get the value of the variable."""
        return self._value

    def set(self, value: _T) -> None:
        """Set the value of the variable."""
        if self._value != value:
            self._value = value
            self.changed.emit(value)

    def bind(self, other: "Variable[_T]") -> None:
        """Bind this variable to another variable."""
        self.changed.connect(other.set)

    def __repr__(self):
        return (
            f"<Variable '{self.objectName()}' of component '{self.__component_name}' "
            f"(current value: {str(self._value)[:20]})>"
        )


def _find_signal_annotations(attrs: dict[str, Any]) -> dict[str, int]:
    """Find all signal annotations in the class attributes.

    Args:
        attrs: Class attributes dictionary.

    Returns:
        Dictionary of signal name and number of arguments.
    """
    ret_val = {}
    for key, value in attrs.get("__annotations__", {}).items():
        # Value is a Signal type hint, so need to get the actual type
        # out of it. This is needed for signals with no arguments, since
        # it's invalid syntax to write `Signal[]` with no arguments to
        # the square brackets. However this means the value is the
        # actual type not a _GenericAlias, so use it as the default arg.
        underlying_value = getattr(value, "__origin__", value)
        if underlying_value and issubclass(underlying_value, Signal):
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


@dataclass
class _VariableMarker:
    """Marker to hold the default value on class variable."""

    name: str
    default_value: Any


def use_state(default_value: _T) -> Variable[_T]:
    """Declare a state variable.

    This is intended to be used as a class variable. The default value
    will be used by all component instances, referring to the same
    value.
    """
    # This is the wrong type but assert it so that IDEs give completion
    # based on the expected return type.
    return _VariableMarker(name="<unset>", default_value=default_value)


def _find_variable_markers(obj: object) -> list[_VariableMarker]:
    """Find instances of use_state in the class.

    Args:
        obj: The object to search.

    Returns:
        Dictionary of variable name and variable marker.
    """
    ret_val: list[_VariableMarker] = []
    for name in dir(obj):
        value = getattr(obj, name)
        if isinstance(value, _VariableMarker):
            value.name = name  # Set the name now we have access to it.
            ret_val.append(value)
    return ret_val


@dataclass
class _EffectMarker:
    """Marker to hold the dependencies of an effect."""

    name: str
    dependencies: list[_VariableMarker]


_EFFECT_MARKER_KEY = "__effect_marker__"


def effect(*dependencies: Variable[Any]):
    """Decorator to mark a method as an effect.

    Args:
        dependencies: List of dependencies for the effect.
    """

    def decorator(func: Callable) -> Callable:
        marker = _EffectMarker(name=func.__name__, dependencies=list(dependencies))
        setattr(func, _EFFECT_MARKER_KEY, marker)
        return func

    return decorator


def _find_effect_markers(obj: object) -> list[_EffectMarker]:
    """Find instances of effect in the class.

    Args:
        obj: The object to search.

    Returns:
        Dictionary of effect name and effect marker.
    """
    ret_val: list[_EffectMarker] = []
    for name in dir(obj):
        value = getattr(obj, name)
        if marker := getattr(value, _EFFECT_MARKER_KEY, None):
            assert marker.name == name, "Effect name mismatch"
            ret_val.append(marker)
    return ret_val


_COMPONENT_STYLESHEET_RESET = {
    "background-color": "transparent",
    "border-radius": "0px",
    "border": "none",
    "margin": "0px",
    "padding": "0px",
}
"""Prevent Qt's unexpected behavior from inheriting parent's style."""


class Component(QtWidgets.QWidget, metaclass=_ComponentMeta):
    """Base class for all widgets."""

    sx = use_state({})

    def __init__(self) -> None:
        super().__init__()

        self.__instantiate_variables()
        self.__bind_effects()

        # Make qt stylesheets work properly!
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def __instantiate_variables(self) -> None:
        """Create Variable instances from class variables."""
        for marker in _find_variable_markers(self):
            variable = Variable(marker.default_value, marker.name, type(self).__name__)
            variable.setParent(self)
            setattr(self, marker.name, variable)

    def __bind_effects(self) -> None:
        """Bind effects to the newly created variables."""
        for effect_marker in _find_effect_markers(self):
            # Get the function object from the class.
            func = getattr(self, effect_marker.name)
            for dependency in effect_marker.dependencies:
                # Find the corresponding variable object.
                variable = getattr(self, dependency.name, None)
                if not isinstance(variable, Variable):
                    raise RuntimeError(
                        f"Effect dependencies can only be Variables, found "
                        f"{type(variable).__name__} for '{dependency.name}' "
                        f"on effect '{effect_marker.name}'"
                    )
                variable.changed.connect(func)
            # Call the function to apply the initial state. The timer
            # ensures the derived class's constructor is finished first.
            QtCore.QTimer.singleShot(0, func)

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

    @effect(sx)
    def _apply_sx(self):
        """Apply the sx property to the widget."""
        sx = _COMPONENT_STYLESHEET_RESET.copy()
        sx.update(self.sx.get())
        self.setStyleSheet(";".join(map(":".join, sx.items())))
