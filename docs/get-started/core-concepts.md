# Core Concepts

## Aim

This library aims to provide a set of components that make it easy to
build modern desktop apps in Qt following the
[Material 3](http://m3.material.io/) design system.

## Conventions

The coding style leverages Python conventions and draws some inspiration
from modern frontend libraries, building on the robust and
well-established core concepts of Qt. Where decisions have been made
that differ from Qt conventions, they are above all in service of the
development experience.

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

### Properties Without Getter Methods

Properties can be accessed with member variables instead of getter
methods.

This aids debugging by immediately showing variable values when
inspecting objects.

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

Colors and many other design aspects are defined in terms of a design
token system instead of similar Qt concepts such as QPalette.

This makes it possible to work with the wider variety of colors used in
Material 3 and helps ensure consistency with external design tools.

```python
# Qt convention
from qtpy.QtGui import QPalette
color = QPalette.ColorRole.Base

# Qt Material UI convention
from material_ui.tokens import md_sys_color
color = md_sys_color.surface
```

### Reactive Effects

Interaction states such as hovered, pressed, focused, etc. have their
dependencies defined in a more declarative way than an event driven way.

This reduces the boilerplate code needed to implement more dynamic
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
    def apply_hover_style(self):
        print("hovered" if self.hovered else "not hovered")
```
