# Buttons

**Buttons prompt most actions in a UI**

![buttons](./buttons.gif)

## Usage

```python
from material_ui.buttons import ElevatedButton
# also available: FilledButton, FilledTonalButton, OutlinedButton, TextButton

button = ElevatedButton()
button.text = "Hello"
button.clicked.connect(lambda: print("Clicked!"))
```

## API

### Properties

| Name   | Type  | Description                                                               |
| ------ | ----- | ------------------------------------------------------------------------- |
| `text` | `str` | Text to display inside the button, indicating the action it will perform. |

### Signals

| Name      | Description                         |
| --------- | ----------------------------------- |
| `clicked` | Emitted when the button is clicked. |
