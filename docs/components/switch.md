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

| Name       | Type   | Description                      |
| ---------- | ------ | -------------------------------- |
| `selected` | `bool` | Whether the switch is on or off. |

### Signals

| Name               | Description                               |
| ------------------ | ----------------------------------------- |
| `change_requested` | Emitted when the user toggles the switch. |

