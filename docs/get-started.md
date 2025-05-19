# Get Started

To get started, install the package into your Python environment using pip:

```
pip install qt-material-ui
```

You will then need to provide your own Qt installation, since this library is using [qtpy](https://pypi.org/project/QtPy/) to work with multiple versions of Qt. If you don't already have Qt installed, you can install PySide6 with pip as well:

```
pip install PySide6
```

## State Management

```python
from material_ui import use_state, Component, Switch

class TV(Component):
    is_powered_on = use_state(False)

    def __init__(self):
        super().__init__()

        status_label = Typography()

        power_switch = Switch(
            selected=self.is_powered_on,
            on_change=self.set_state(self.is_powered_on),
        )

        # TODO: add widgets to a layout?
    @effect(is_powered_on)
    def update_status_label(self):
        status_label.text = f"TV is {'on' if self.is_powered_on.get() else 'off'}"
```
