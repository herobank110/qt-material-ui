# Get Started

WIP

## State Management

```python
from material_ui import use_state, Component, Switch

class TV(Component):
    is_powered_on = use_state(False)

    def __init__(self):
        super().__init__()

        status_label = Typography()
        status_label.text.bind(
            lambda: f"TV is {'on' if self.is_powered_on.get() else 'off'}",
            [self.is_powered_on]
        )

        power_switch = Switch()
        power_switch.selected.bind(self.is_powered_on)
        power_switch.change_requested.connect(self.is_powered_on.set)

        # TODO: add widgets to a layout?
```
