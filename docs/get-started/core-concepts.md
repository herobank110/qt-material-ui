# Core Concepts

This project aims to provide a set of components that make it easy to
build modern desktop apps in Qt following the
[Material Design 3](http://m3.material.io/) system.

Various decisions are aligned more with Python conventions, with some
inspiration also drawn from modern frontend libraries, rather than Qt
conventions. However, Qt provides many useful concepts and well-tested
data structures which this library uses throughout.

Inspiration from other libraries:

- [Material UI (React library)](https://mui.com/)
- [Material Web (web components)](https://material-web.dev/)

## Key Differences from Qt

### Naming Conventions

Variables and functions are named with snake_case instead of
camelCase.

The word 'component' is generally preferred over 'widget'.

The Q prefix is not used to help distinguish from the Qt API.

### Properties vs Getter Methods

Properties can be accessed with member variables instead of getter
methods.

This saves some keyboard typing.

```python
# Qt convention
text = button.text()

# Qt Material UI convention
text = button.text
```

### Styling In Python

Styles are defined with a Python dictionary instead of a stylesheet
string or separate QSS files.

This enables the full flexibility of Python expressions to compute the
style without needing to manually convert values to strings.

```python
# Qt convention
button.setStyleSheet("background-color: red; color: white;")

# Qt Material UI convention
button.sx = {"background-color": "red", "color": "white"}
```

### Style Inheritance

In Qt, a child widget inherits the style of its parent widget. This
library resets the style of each component before applying any
additional styling.

This protects components from unintended 'style leaking'.

### Interactive Effects

Interaction states such as hovered, pressed, focused, etc. have their
side effects defined in a more declarative way than an event driven
way.

This makes it easier to implement more interactive components.

```python
# Qt convention

from qtpy.QtCore import QEvent
from qtpy.QtGui import QEnterEvent
from qtpy.QtWidgets import QWidget

class Button(QWidget):
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
