# Text Fields

**Text fields let users enter text into a UI.**

![text-fields](./text-fields.gif)

## Usage

```python
from material_ui.text_fields import FilledTextField

text_field = FilledTextField()
text_field.label = "Name"
```

## API

### Properties

| Name    | Type  | Default | Description                      |
| ------- | ----- | ------- | -------------------------------- |
| `label` | `str` | `""`    | Floating label text.             |
| `value` | `str` | `""`    | Current value of the text field. |

### Signals

| Name        | Arguments    | Description                     |
| ----------- | ------------ | ------------------------------- |
| `on_change` | `value: str` | Emitted when the value changed. |
