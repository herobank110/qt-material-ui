# Buttons

**Buttons prompt most actions in a UI**

![buttons](./buttons.gif)

## Usage

```python
from material_ui.buttons import ElevatedButton
# also available: FilledButton, FilledTonalButton, OutlinedButton, TextButton

ElevatedButton(
    text="Hello",
    clicked=lambda: print("Clicked!"),
)
```

## API

### Properties

| Name   | Type  | Default | Description                                                               |
| ------ | ----- | ------- | ------------------------------------------------------------------------- |
| `text` | `str` | `""`    | Text to display inside the button, indicating the action it will perform. |

### Signals

| Name      | Arguments | Description                         |
| --------- | --------- | ----------------------------------- |
| `clicked` | n/a       | Emitted when the button is clicked. |
