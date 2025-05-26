# Checkbox

**Checkboxes allow users to select one or more items from a set.**

![demonstration](./checkbox.gif)

## Usage

```python
from material_ui import Checkbox

checkbox = Checkbox()
```

## API

### Properties

| Name            | Type   | Default | Description                                        |
| --------------- | ------ | ------- | -------------------------------------------------- |
| `selected`      | `bool` | `False` | Whether the checkbox is checked.                   |
| `indeterminate` | `bool` | `False` | Whether the checkbox is in an indeterminate state. |

### Signals

| Name        | Arguments     | Description                                 |
| ----------- | ------------- | ------------------------------------------- |
| `on_change` | `value: bool` | Emitted when the user toggles the checkbox. |
