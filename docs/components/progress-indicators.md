# Progress Indicators

Progress indicators inform users about the status of ongoing processes,
such as loading an app or submitting a form.

![progress indicators](./progress-indicators.gif)

## Usage

```python
from material_ui.progress_indicators import CircularProgress, LinearProgress

spinner = CircularProgress()
spinner.value = 0.5

loading_bar = LinearProgress()
loading_bar.indeterminate = True
```

## API

### Properties

| Name            | Type    | Default | Description                                                |
| --------------- | ------- | ------- | ---------------------------------------------------------- |
| `value`         | `float` | `0.0`   | Progress percentage, in range [0, 1].                      |
| `indeterminate` | `bool`  | `False` | Whether the progress is indeterminate (looping animation). |

### Signals

N/A
