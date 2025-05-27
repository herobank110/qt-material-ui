# Core Concepts

## Aim

This library aims to provide a set of components for the Qt Widgets
framework following the [Material 3](http://m3.material.io/) design
system.

## Conventions

The coding style leverages Python conventions and draws some inspiration
from modern frontend libraries, building on the robust and
well-established core concepts of Qt.

Inspiration from other libraries:

- [Material UI (React library)](https://mui.com/)
- [Material Web (web components)](https://material-web.dev/)

### Naming Conventions

Variables and functions are named with snake case instead of
camel case.

This avoids linting issues with standard Python tools.

```python
# Qt convention
fontSize

# Qt Material UI convention
font_size
```

### Properties With Member Variables

Properties can be accessed with member variables instead of getter
methods.

This means actual values are shown instead of method objects when
debugging.

```python
# Qt convention
text = button.text()

# Qt Material UI convention
text = button.text
```

### Styling In Python

Styles are defined with a Python dictionary instead of a stylesheet
string or separate QSS files.

This unlocks the flexibility of Python expressions when computing the
style.

```python
# Qt convention
button.setStyleSheet("background-color: red; color: white;")

# Qt Material UI convention
button.sx = {"background-color": "red", "color": "white"}
```

### Style Inheritance

Component styles don't automatically inherit the styles set in the
parent.

This protects components from unintended 'style leaking'.

```python
# Qt convention
parent = QWidget()
parent.setStyleSheet("border: 1px solid black;")
child = QWidget()
child.setParent(parent)  # child gets a border too

# Qt Material UI convention
parent = Component()
parent.sx = {"border": "1px solid black"}
child = Component()
child.setParent(parent)  # child won't get a border
```

### Design Tokens

Colors and some other design aspects are defined with design tokens
instead of similar Qt concepts such as QPalette.

This enables support for the wider variety of styling using in Material
Design.

```python
# Qt convention
from qtpy.QtGui import QPalette
color = QPalette.ColorRole.Base

# Qt Material UI convention
from material_ui.tokens import md_sys_color
color = md_sys_color.surface
```

## Additional Features

Some features were created during the development of this library to
improve the development experience.

There may also be additional benefit from these features by writing
custom components. However, the library components are designed to be
fully functional within any standard Qt widget.

### Type Safe Signals

Signals are defined with type annotations that enable type checkers to
check the arguments of connected callbacks and emit calls.

This improves code safety over native Qt widgets.

```python
# Qt convention

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget

class Button(QWidget):
    foo = Signal(str)

Button().foo.emit(1)
# mypy unable to detect any error


# Qt Material UI convention

from material_ui.component import Component, Signal

class Button(Component):
    foo: Signal[str]

Button().foo.emit(1)

# caught by mypy:
# error: Argument 1 to "emit" of "Signal" has incompatible type "int"; expected "str"  [arg-type]
```

### Reactive Effects

Component states such as hovered, pressed, etc. have code dependencies
defined in a more declarative than event driven way.

This reduced the boilerplate code needed to implement dynamic
components.

```python
# Qt convention

from qtpy.QtCore import QEvent
from qtpy.QtGui import QEnterEvent
from qtpy.QtWidgets import QWidget

class Button(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.apply_hover_style(hovered=False)

    def enterEvent(self, event: QEnterEvent) -> None:
        super().enterEvent(event)
        self.apply_hover_style(hovered=True)

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self.apply_hover_style(hovered=False)

    def apply_hover_style(self, hovered: bool) -> None:
        print("hovered" if hovered else "not hovered")

# Qt Material UI convention

from material_ui.component import Component, effect

class Button(Component):
    @effect(Component.hovered)
    def apply_hover_style(self) -> None:
        print("hovered" if self.hovered else "not hovered")
```
