# ComboBox

**ComboBoxes allow users to select from a dropdown list.**

![demonstration](./combobox.gif)

## Usage

```python
from material_ui import ComboBox

combo = ComboBox()
combo.items = ["Option 1", "Option 2", "Option 3"]
combo.label = "Select an option"
```

## API

### Properties

| Name     | Type        | Default | Description                              |
| -------- | ----------- | ------- | ---------------------------------------- |
| `label ` | `str`       | `""`    | Label for the textfield of the combobox. |
| `value`  | `str`       | `""`    | Currently selected value.                |
| `items`  | `list[str]` | `[]`    | List of items to select from.            |

### Signals

| Name        | Arguments    | Description                       |
| ----------- | ------------ | --------------------------------- |
| `on_change` | `value: str` | Called when the value is changed. |
