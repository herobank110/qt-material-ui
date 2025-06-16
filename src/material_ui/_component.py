"""Internal widgets common functionality and helpers for Qt Widgets."""

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any, Generic, TypeVar, cast, get_args, overload

from qtpy.QtCore import (
    Property,  # pyright: ignore  # noqa: PGH003
    QEasingCurve,
    QEvent,
    QMargins,
    QObject,
    QPropertyAnimation,
    QSize,
    Qt,
    QTimer,
)
from qtpy.QtCore import (
    Signal as QtSignal,  # pyright: ignore  # noqa: PGH003
)
from qtpy.QtGui import QEnterEvent, QFocusEvent, QMouseEvent, QResizeEvent
from qtpy.QtWidgets import QGraphicsOpacityEffect, QVBoxLayout, QWidget
from typing_extensions import TypeIs, TypeVarTuple, Unpack

from material_ui._utils import StyleDict, convert_sx_to_qss, undefined
from material_ui.hook import Hook
from material_ui.theming.theme_hook import ThemeHook
from material_ui.tokens._utils import DesignToken, resolve_token_or_value

_Ts = TypeVarTuple("_Ts", default=Unpack[tuple[()]])


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


@dataclass
class _TransitionConfig:
    """Transition properties for a state variable."""

    duration_ms: int
    easing: QEasingCurve.Type


class State(QObject, Generic[_T]):
    """Type safe property wrapper object.

    Creates a Qt property with a getter and setter and changed signal.

    Also used for one-way data binding and defined dependencies between
    variables.
    """

    changed: Signal[_T] = QtSignal("QVariant")  # type: ignore[assignment]

    def __init__(self, default_value: _T, name: str) -> None:
        super().__init__()
        self.setObjectName(name)
        self._value = default_value
        self._default_value = default_value
        self.transition: _TransitionConfig | None = None
        self._active_animation: QPropertyAnimation | None = None
        self._is_bound = False

    def get_value(self) -> _T:
        """Get the value of the variable."""
        return self._value

    def set_value(self, value: _T, *, _from_binding: bool = False) -> None:
        """Set the value of the variable.

        If the value changed, the changed signal is emitted.

        If the state is bound to another state, this function has no
        effect.

        Args:
            value: New value to use.
            _from_binding: Internal - whether the value was set from
                the state it is bound to.
        """
        if self._is_bound and not _from_binding:
            return
        if self._value != value:
            self._value = value
            self.changed.emit(value)

    def animate_to(
        self,
        value: _T,
        duration_ms: int,
        easing: QEasingCurve.Type,
    ) -> None:
        """Transition from current value to a new value.

        Args:
            value: The value to animate to.
            duration_ms: The duration of the animation in milliseconds.
            easing: The easing curve to use for the animation.
        """
        self._clear_active_animation()
        animation = QPropertyAnimation()
        animation.setParent(self)
        animation.setTargetObject(self)
        animation.setPropertyName(self._QT_PROPERTY_NAME.encode())
        animation.setDuration(duration_ms)
        animation.setEasingCurve(easing)
        animation.setStartValue(self._value)
        animation.setEndValue(value)
        animation.start()
        animation.finished.connect(self._clear_active_animation)
        self._active_animation = animation

    def _clear_active_animation(self) -> None:
        if self._active_animation:
            self._active_animation.setParent(None)
            self._active_animation.deleteLater()
            self._active_animation = None

    def set_transition(self, config: _TransitionConfig) -> None:
        """Automatically animate to the new value when set."""
        self.transition = config

    def bind(self, other: "State[_T]") -> None:
        """Bind this variable to another variable."""
        other.changed.connect(partial(self.set_value, _from_binding=True))
        self.set_value(other.get_value())  # Set initial state.
        self._is_bound = True
        # TODO: track object deletion

    def __repr__(self) -> str:
        parent_name = type(self.parent()).__name__ if self.parent() else "no-parent"
        return (
            f"<State '{self.objectName()}' of component '{parent_name}' "
            f"(current value: {str(self._value)[:20]})>"
        )

    _qt_property = Property("QVariant", get_value, set_value, None, "")
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
    ret_val: dict[str, int] = {}
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


class _ComponentMeta(type(QObject)):  # type: ignore[misc]
    """Meta class for all widgets."""

    def __new__(cls, name: str, bases: Any, attrs: Any) -> type:
        # Convert Signal annotations to actual Qt Signal objects.
        # Use QVariant to avoid runtime type checking by Qt. Can't
        # remember exact examples but it may fail for certain types.
        attrs.update(
            {
                key: QtSignal(*["QVariant"] * num_args)
                for key, num_args in _find_signal_annotations(attrs).items()
            },
        )
        return super().__new__(cls, name, bases, attrs)


@dataclass
class _StateMarker:
    """Marker to hold the default value on class variable."""

    name: str
    default_value: Any
    transition: int | None = None
    easing: QEasingCurve.Type = QEasingCurve.Type.Linear


def use_state(
    default_value: _T,
    transition: int | None = None,
    easing: QEasingCurve.Type = QEasingCurve.Type.Linear,
) -> _T:
    """Declare a state variable.

    This is intended to be used as a class variable. The default value
    will be used by all component instances, referring to the same
    value.

    Example:
        class MyComponent(Component):
            my_state = use_state("hello")

    Args:
        default_value: The default value of the state variable. This
            also sets the type of the variable, so it may be beneficial
            to use `cast` to show the full type (eg for optional values
            with initial state of None).
        transition: Optional transition duration, in milliseconds.
        easing: Optional easing curve to use for the transition.

    Returns:
        A marker object that will be replaced with the actual state once
        the object is constructed. The type annotation is intentionally
        incorrect to aid type annotations on the class variables.
        However it's only valid to use it in object instances, not as a
        static variable.
    """
    # This is the wrong type but assert it so that IDEs give completion
    # based on the expected return type.
    return _StateMarker(
        name="<unset>",
        default_value=default_value,
        transition=transition,
        easing=easing,
    )  # type: ignore[return-value]


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


_EffectDependency = _StateMarker | type[Hook]
"""Effect dependency type."""


@dataclass
class _EffectMarker:
    """Marker to hold the dependencies of an effect."""

    name: str
    dependencies: list[_EffectDependency]


_EFFECT_MARKER_KEY = "__effect_marker__"


EffectFn = Callable[[Any], None]


class EffectDependencyError(RuntimeError):
    """Raised when the effect dependencies are invalid."""


def effect(*dependencies: Any) -> Callable[[EffectFn], EffectFn]:
    """Decorator to mark a method as an effect.

    The function will be called when the dependencies change, and also
    on the initial state.

    Args:
        dependencies: List of dependencies for the effect. These must be
            class variables marked with `use_state`.

    Returns:
        Decorated method.
    """
    # Special handling for Qt built in properties.
    # TODO: shadow these with actual states?
    dependencies_list = [
        x
        if isinstance(x, _StateMarker)
        else _StateMarker(name="_size", default_value=QSize())
        if x is QWidget.size
        else x
        for x in dependencies
    ]

    # Validate dependency types.
    for dependency in dependencies_list:
        if not _is_valid_effect_dependency(dependency):
            msg = f"Invalid dependency for effect: {dependency} ({type(dependency)})"
            raise EffectDependencyError(msg)

    def decorated(func: EffectFn) -> EffectFn:
        marker = _EffectMarker(name=func.__name__, dependencies=dependencies_list)
        setattr(func, _EFFECT_MARKER_KEY, marker)
        return func

    return decorated


def _is_valid_effect_dependency(dependency: Any) -> TypeIs[_EffectDependency]:
    return isinstance(dependency, _StateMarker) or (
        isinstance(dependency, type) and issubclass(dependency, Hook)
    )


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
            if marker.name != name:
                msg = "Effect name mismatch"
                raise RuntimeError(msg)
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


_LAST_ACCESSED_STATE_KEY = "__mui_last_accessed_attr__"


def _track_last_accessed_state(state: State[Any]) -> None:
    frame = inspect.currentframe()
    caller_frame = frame and frame.f_back
    caller_frame = caller_frame and caller_frame.f_back
    if caller_frame:
        caller_frame.f_locals[_LAST_ACCESSED_STATE_KEY] = state


def _pop_last_accessed_state(value: _T) -> State[_T] | None:
    # Check if we can bind to another object's state.
    # TODO: what if there are multiple intermediate stack frames?
    #   should it be global?
    frame = inspect.currentframe()
    caller_frame = frame and frame.f_back
    caller_frame = caller_frame and caller_frame.f_back
    state = (
        # Pop so it can't be rebound accidentally.
        caller_frame.f_locals.pop(_LAST_ACCESSED_STATE_KEY, None)
        if caller_frame
        else None
    )
    # Ensure it's the same value. This isn't always reliable but should
    # work for now...
    # TODO: additional checks? check id of values? types? code lineno? not itself?
    if state and isinstance(state, State) and state.get_value() is value:
        return cast("State[_T]", state)
    return None


class Component(QWidget, metaclass=_ComponentMeta):
    """Base class for all widgets."""

    sx = use_state(cast("StyleDict", {}))

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
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, on=True)

        self.should_propagate_click = True
        """Whether the click event should be propagated to the parent widget."""

    def __instantiate_state_variables(self) -> None:
        """Create State instances from class variables."""
        for marker in _find_state_markers(self):
            state = State(marker.default_value, marker.name)
            state.setParent(self)
            setattr(self, marker.name, marker.default_value)
            # Propagate the internal state value to the mem var proxy.
            # This won't cause an infinite loop since the setter checks
            # if the value is different. It will eventually stabilize.
            # Use super so that it doesn't try to call the set_value of
            # the state again.
            state.changed.connect(partial(super().__setattr__, marker.name))
            # Apply transition if specified.
            if marker.transition:
                state.set_transition(
                    _TransitionConfig(marker.transition, marker.easing),
                )

    def __getattribute__(self, name: str) -> Any:
        actual_value = super().__getattribute__(name)
        if name in {
            Component._find_state.__name__,
            Component.findChild.__name__,
        }:
            # Prevent recursion error. These are used below.
            return actual_value
        state = self._find_state(name)
        if state:
            # A state variable was accessed. Track it for binding.
            _track_last_accessed_state(state)
        return actual_value

    def __setattr__(self, name: str, value: Any) -> None:
        if state := self._find_state(name):
            if other_state := _pop_last_accessed_state(value):
                state.bind(other_state)
            elif state.transition:
                state.animate_to(
                    value,
                    state.transition.duration_ms,
                    state.transition.easing,
                )
            else:
                state.set_value(value)
        super().__setattr__(name, value)

    def _find_state(self, name: str) -> State[Any] | None:
        """Find state variable by name."""
        return self.findChild(
            cast("type[State[Any]]", State),
            name,
            Qt.FindChildOption.FindDirectChildrenOnly,
        )

    @overload
    def set_state(self, name: str) -> Callable[[Any], None]: ...

    @overload
    def set_state(self, name: str, value: Any) -> None: ...

    def set_state(
        self,
        name: str,
        value: Any = undefined,
    ) -> Callable[[Any], None] | None:
        """Set a state variable by name.

        Args:
            name: Name of the state variable.
            value: Value to set if needed.

        Returns:
            If no value is specified, a function is returned that can be
            used to set the value later.
            If a value is specified, None is returned.

        Raises:
            AttributeError: If no state with the given name exists.
        """
        state = self._find_state(name)
        if state is None:
            raise AttributeError
        if value is undefined:
            return state.set_value
        state.set_value(value)
        return None

    def __bind_effects(self) -> None:
        """Bind effects to the newly created variables."""
        for effect_marker in _find_effect_markers(self):
            # Get the function object from the class.
            func = getattr(self, effect_marker.name)
            for dependency in effect_marker.dependencies:
                if isinstance(dependency, _StateMarker):
                    # Find the corresponding variable object.
                    state = self._find_state(dependency.name)
                    if not isinstance(state, State):
                        msg = f"Invalid dependency for {dependency.name}: '{state}'"
                        raise TypeError(msg)
                    state.changed.connect(func)
                else:
                    # Dependency is a hook, so connect to its on_change signal.
                    hook_instance = dependency.get()
                    hook_instance.on_change.connect(func)
            # Call the function to apply the initial state. The timer
            # ensures the derived class's constructor is finished first.
            QTimer.singleShot(0, func)

    def overlay_widget(
        self,
        widget: QWidget,
        margins: QMargins | None = None,
        *,
        center: bool = False,
    ) -> None:
        """Overlay a widget on top of this widget.

        Ownership will also be set to this widget.
        """
        widget.setParent(self)
        if self.layout() is not None:
            msg = "Multiple overlay widgets not supported yet"
            raise NotImplementedError(msg)
        # TODO: add some other kind of 'overlay' layout similar to graphics anchors?
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(margins or QMargins())
        if center:
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget)

    def set_transition(
        self,
        state: Any,
        duration_ms: int,
        easing: QEasingCurve.Type = QEasingCurve.Type.Linear,
    ) -> None:
        """Set a transition for a state variable.

        Args:
            state: Target state variable.
            duration_ms: Animation duration, in milliseconds.
            easing: Easing curve to use for the animation.
        """
        if state_obj := _pop_last_accessed_state(state):
            state_obj.set_transition(_TransitionConfig(duration_ms, easing))

    @effect(sx, ThemeHook)
    def _apply_sx(self) -> None:
        """Apply the sx property to the widget."""
        sx = {**_COMPONENT_STYLESHEET_RESET, **self.sx}
        # Special handling for opacity - pass to a graphics effect.
        if (opacity := sx.pop("opacity", None)) is not None:
            if not isinstance(opacity, (float, DesignToken)):
                raise TypeError
            self._apply_opacity_from_sx(opacity)
        qss = convert_sx_to_qss(sx)
        self.setStyleSheet(qss)

    def _apply_opacity_from_sx(self, opacity: float | DesignToken) -> None:
        if effect := self.graphicsEffect():
            # Reuse existing effect unless one is already set - Qt can
            # only have one.
            if not isinstance(effect, QGraphicsOpacityEffect):
                raise RuntimeError
        else:
            # Create a new effect.
            effect = QGraphicsOpacityEffect(self)
            self.setGraphicsEffect(effect)
        resolved_opacity = resolve_token_or_value(opacity)
        if not isinstance(resolved_opacity, float):
            raise TypeError
        effect.setOpacity(resolved_opacity)

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        self._size = self.size()

    @effect(QWidget.size)
    def _apply_size(self) -> None:
        """Apply the size property to the widget."""
        self.resize(self.size())

    def focusInEvent(self, event: QFocusEvent) -> None:  # noqa: N802
        self.focused = True
        return super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:  # noqa: N802
        self.focused = False
        return super().focusOutEvent(event)

    def setFocusProxy(self, w: QWidget | None) -> None:  # noqa: N802
        # Intercept the focus proxy to listen to focus events correctly,
        # since Qt won't propagate the focus In/Out events to this
        # widget.
        if w:
            # TODO: edge cases, remove filter from previous focus proxy, unit tests
            w.installEventFilter(self)

        # Wrong Qt type annotation - should be QWidget | None.
        return super().setFocusProxy(w)  # type: ignore[arg-type]

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802
        if watched is self.focusProxy():
            # Intercept the focus events from the focus proxy.
            if event.type() == QEvent.Type.FocusIn:
                self.focusInEvent(cast("QFocusEvent", event))
                return False  # Focus proxy should handle it too.
            if event.type() == QEvent.Type.FocusOut:
                self.focusOutEvent(cast("QFocusEvent", event))
                return False  # Focus proxy should handle it too.
        return super().eventFilter(watched, event)

    hovered = use_state(False)
    pressed = use_state(False)
    clicked: Signal

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = True
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = False
            mouse_inside = self.rect().contains(event.pos())
            if mouse_inside:
                self.clicked.emit()
                if not self.should_propagate_click:
                    return None
        return super().mouseReleaseEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:  # noqa: N802
        self.hovered = True
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:  # noqa: N802
        self.hovered = False
        return super().leaveEvent(event)
