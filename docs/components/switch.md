# Switch

**Switches toggle the selection of an item on or off**

![switch](./switch.gif)

## Usage

```python
from material_ui import Switch

switch = Switch()
```

## API

### Properties

| Name       | Type   | Default | Description                      |
| ---------- | ------ | ------- | -------------------------------- |
| `selected` | `bool` | `False` | Whether the switch is on or off. |

### Signals

| Name        | Arguments     | Description                               |
| ----------- | ------------- | ----------------------------------------- |
| `on_change` | `value: bool` | Emitted when the user toggles the switch. |
