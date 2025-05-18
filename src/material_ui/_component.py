"""Internal widgets common functionality and helpers for Qt Widgets."""

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, cast, get_args
from typing_extensions import TypeVarTuple, Unpack
from qtpy.QtCore import (
    QEvent,
    QObject,
    Property,
    QTimer,
    Signal as QtSignal,
    QMargins,
    QSize,
    Qt,
    QEasingCurve,
    QPropertyAnimation,
)
from qtpy.QtGui import QFocusEvent, QResizeEvent
from qtpy.QtWidgets import QWidget, QVBoxLayout

from material_ui._utils import StyleDict, convert_sx_to_qss


_Ts = TypeVarTuple("_Ts")


# TODO: should this be a protocol?
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


class State(QObject, Generic[_T]):
    """Type safe property wrapper object.

    Creates a Qt property with a getter and setter and changed signal.

    Also used for one-way data binding and defined dependencies between
    variables.
    """

    changed: Signal[_T] = QtSignal("QVariant")

    def __init__(self, default_value: _T, name: str, component_name: str) -> None:
        super().__init__()
        self.setObjectName(name)
        self.__component_name = component_name
        self._value = default_value
        self._default_value = default_value

    def get(self) -> _T:
        """Get the value of the variable."""
        return self._value

    def set(self, value_or_fn: _T | Callable[[_T], _T]) -> None:
        """Set the value of the variable.

        Args:
            value_or_fn: Either a value directly, or a function that
                takes the current value as input and returns a new one.
        """
        value: _T = (
            value_or_fn(self._value)
            if hasattr(value_or_fn, "__call__")
            else value_or_fn
        )
        if self._value != value:
            self._value = value
            self.changed.emit(value)

    def animate_to(
        self, value: _T, duration_ms: int, easing: QEasingCurve.Type
    ) -> None:
        """Transition from current value to a new value.

        Args:
            value: The value to animate to.
            duration_ms: The duration of the animation in milliseconds.
            easing: The easing curve to use for the animation.
        """
        animation = QPropertyAnimation()
        animation.setParent(self)
        animation.setTargetObject(self)
        animation.setPropertyName(self._QT_PROPERTY_NAME.encode())
        animation.setDuration(duration_ms)
        animation.setEasingCurve(easing)
        animation.setStartValue(self._value)
        animation.setEndValue(value)
        animation.start()

    def bind(self, other: "State[_T]") -> None:
        """Bind this variable to another variable."""
        other.changed.connect(self.set)
        self.set(other.get())  # Set initial state.
        # TODO: track object deletion

    def __repr__(self):
        return (
            f"<State '{self.objectName()}' of component '{self.__component_name}' "
            f"(current value: {str(self._value)[:20]})>"
        )

    _qt_property = Property("QVariant", get, set)
    """This is used by Qt to drive the animation."""

    _QT_PROPERTY_NAME = "_qt_property"
    """Name of the Qt property."""


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


class _ComponentMeta(type(QObject)):
    """Meta class for all widgets."""

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> type:
        # Convert Signal annotations to actual Qt Signal objects.
        # Use QVariant to avoid runtime type checking by Qt. Can't
        # remember exact examples but it may fail for certain types.
        attrs.update(
            {
                key: QtSignal(*["QVariant"] * num_args)
                for key, num_args in _find_signal_annotations(attrs).items()
            }
        )
        return super().__new__(cls, name, bases, attrs)


@dataclass
class _StateMarker:
    """Marker to hold the default value on class variable."""

    name: str
    default_value: Any


def use_state(default_value: _T) -> State[_T]:
    """Declare a state variable.

    This is intended to be used as a class variable. The default value
    will be used by all component instances, referring to the same
    value.
    """
    # This is the wrong type but assert it so that IDEs give completion
    # based on the expected return type.
    return _StateMarker(name="<unset>", default_value=default_value)


def _find_state_markers(obj: object) -> list[_StateMarker]:
    """Find instances of use_state in the class.

    Args:
        obj: The object to search.

    Returns:
        List of state markers.
    """
    ret_val: list[_StateMarker] = []
    for name in dir(obj):
        value = getattr(obj, name)
        if isinstance(value, _StateMarker):
            value.name = name  # Set the name now we have access to it.
            ret_val.append(value)
    return ret_val


@dataclass
class _EffectMarker:
    """Marker to hold the dependencies of an effect."""

    name: str
    dependencies: list[_StateMarker]


_EFFECT_MARKER_KEY = "__effect_marker__"


def effect(*dependencies: State[Any]) -> Callable[[Callable], Callable]:
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


_COMPONENT_STYLESHEET_RESET: StyleDict = {
    "background-color": "transparent",
    "border-radius": "0px",
    "border": "none",
    "margin": "0px",
    "padding": "0px",
}
"""Prevent Qt's unexpected behavior from inheriting parent's style."""


class Component(QWidget, metaclass=_ComponentMeta):
    """Base class for all widgets."""

    sx = use_state(cast(StyleDict, {}))

    focused = use_state(False)
    """State version of Qt's `focus` property.

    This is only for reading the focus state and creating dependencies.
    To set focus, use Qt's built in focus handling functions for more
    flexibility.
    """

    _size = use_state(QSize())
    """Internal state for Qt `size` property."""

    def __init__(self) -> None:
        super().__init__()

        self.__instantiate_state_variables()
        self.__bind_effects()

        # Make qt stylesheets work properly!
        self.setAttribute(Qt.WA_StyledBackground, True)

    def __instantiate_state_variables(self) -> None:
        """Create State instances from class variables."""
        for marker in _find_state_markers(self):
            variable = State(marker.default_value, marker.name, type(self).__name__)
            variable.setParent(self)
            setattr(self, marker.name, variable)

    def __setattr__(self, name, value):
        variable = getattr(self, name, None)
        if isinstance(variable, State) and not isinstance(value, State):
            # Shorthand for setting the value of a State variable.
            variable.set(value)
            return
        return super().__setattr__(name, value)

    def __bind_effects(self) -> None:
        """Bind effects to the newly created variables."""
        for effect_marker in _find_effect_markers(self):
            # Get the function object from the class.
            func = getattr(self, effect_marker.name)
            for dependency in effect_marker.dependencies:
                # Special handling for Qt built in properties.
                if dependency is QWidget.size:
                    variable = self._size
                else:
                    # Find the corresponding variable object.
                    variable = getattr(self, dependency.name, None)
                if not isinstance(variable, State):
                    raise RuntimeError(
                        f"Effect dependencies can only be States, found "
                        f"{type(variable).__name__} for '{dependency.name}' "
                        f"on effect '{effect_marker.name}'"
                    )
                variable.changed.connect(func)
            # Call the function to apply the initial state. The timer
            # ensures the derived class's constructor is finished first.
            QTimer.singleShot(0, func)

    def overlay_widget(self, widget: QWidget, margins: QMargins | None = None) -> None:
        """Overlay a widget on top of this widget.

        Ownership will also be set to this widget.
        """
        widget.setParent(self)
        if self.layout() is not None:
            raise NotImplementedError("Multiple overlay widgets not supported yet")
        # TODO: add some other kind of 'overlay' layout similar to graphics anchors?
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(margins or QMargins())
        layout.addWidget(widget)

    @effect(sx)
    def _apply_sx(self):
        """Apply the sx property to the widget."""
        sx = _COMPONENT_STYLESHEET_RESET | self.sx.get()
        qss = convert_sx_to_qss(sx)
        self.setStyleSheet(qss)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._size.set(self.size())

    @effect(_size)
    def _apply_size(self):
        """Apply the size property to the widget."""
        self.resize(self._size.get())

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.focused = True
        return super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.focused = False
        return super().focusOutEvent(event)

    def setFocusProxy(self, w: QWidget | None) -> None:  # noqa: N802
        # Intercept the focus proxy to listen to focus events correctly,
        # since Qt won't propagate the focus In/Out events to this
        # widget.
        if w:
            # TODO: edge cases, remove filter from previous focus proxy, unit tests
            w.installEventFilter(self)

        return super().setFocusProxy(w)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self.focusProxy():
            # Intercept the focus events from the focus proxy.
            if event.type() == QEvent.FocusIn:
                self.focusInEvent(event)
                return False  # Focus proxy should handle it too.
            elif event.type() == QEvent.FocusOut:
                self.focusOutEvent(event)
                return False  # Focus proxy should handle it too.
        return super().eventFilter(watched, event)
