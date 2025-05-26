# Philosophy

The project aims to provide a set of components that make it easy to build
modern desktop apps in Qt following the
[Material Design 3 system](http://m3.material.io/).

Some decisions were made to align with conventions established by modern
frontend libraries such as MUI, rather than traditional Qt conventions.

Core inspiration:

- [Material UI (React library)](https://mui.com/)
- [Material Web (web components)](https://material-web.dev/)

## Key Differences from Qt

### Naming Conventions

Variables and functions are named with snake_case instead of
camelCase.

The word 'component' is generally preferred over 'widget'.

The Q prefix is not used to help distinguish from the Qt API.

### Properties vs Getter Methods

Properties can be accessed with member variables instead of a getter
methods.

This saves some keyboard typing and is more Pythonic.

```python
# Qt style
text = button.text()

# Qt Material UI style
text = button.text
```

### Style Dict vs String

Styles are defined with a Python dictionary instead of a stylesheet
string. This property is named `sx`
([read more](https://mui.com/material-ui/customization/how-to-customize/#the-sx-prop)).

This simplifies the creation of dynamic styles by enabling any Python
expression to be used for the value without string interpolation.

```python
# Qt style
button.setStyleSheet("background-color: red; color: white;")

# Qt Material UI style
button.sx = {"background-color": "red", "color": "white"}
```

### Style Inheritance

In Qt, a child widget inherits the style of its parent widget. This
library resets the style of each component before applying any
additional styling.

This protects components from unintended 'style leaking'.
