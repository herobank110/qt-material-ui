# Typography

**Typography helps make writing legible and beautiful.**

![demonstration](./typography.jpg)

## Basic Usage

```python
from material_ui.typography import Typography

typography = Typography()
typography.variant = "body-medium"
typography.text = "Hello world"
```

## Font

The default font used by Qt Material UI is Roboto. This can be
customized with the design token system.

### Variable Axis

Variable axis is currently used to control font weight, as it enables
greater precision than Qt's own font properties.

Variable axis support is available in Qt 6+.

### Missing Properties

At the time of writing, not all font properties are natively handled by
Qt. The following properties can't be controlled by the design token
system:

- line height
- tracking

As a partial workaround, it's possible to apply padding and margins to
create space around typography.

## Variants

Individual font properties can be set using a variant as a shorthand.

The variant uses a literal string, and is type checked using a `Literal`
type.

If a variant is specified, changing the individual font properties will
have no effect.

```python
# shorthand
typography.variant = "headline-medium"

# full version
from material_ui.tokens import md_sys_typescale
typography.font_family = md_sys_typescale.headline_medium_font
typography.font_size = md_sys_typescale.headline_medium_size
typography.font_weight = md_sys_typescale.headline_medium_weight
```

The full list of available variants is as follows:

- `display-large`
- `display-medium`
- `headline-large`
- `headline-medium`
- `headline-small`
- `title-large`
- `title-medium`
- `title-small`
- `body-large`
- `body-medium`
- `body-small`
- `label-large`
- `label-large-prominent`
- `label-medium`
- `label-medium-prominent`
- `label-small`

## API

### Properties

| Name          | Type                                                                 | Default              | Description                                                  |
| ------------- | -------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------ |
| `text`        | `str`                                                                | `""`                 | The writing to display.                                      |
| `color`       | `DesignToken` \| [`QColor`](https://doc.qt.io/qt-6/qcolor.html)      | `on_surface`         | Text color.                                                  |
| `variant`     | [`TypographyVariant`](#variants) \| `None`                           | `None`               | Typography variant to control the font values from a preset. |
| `font_family` | `DesignToken`                                                        | `body_medium_font`   | Font family.                                                 |
| `font_size `  | `DesignToken`                                                        | `body_medium_size`   | Font size defined by a design token. Units are in DP.        |
| `font_weight` | `DesignToken`                                                        | `body_medium_weight` | Font weight defined by a design token.                       |
| `alignment `  | [`AlignmentFlag`](https://doc.qt.io/qt-6/qt.html#AlignmentFlag-enum) | `0` | Text alignment within the widget's geometry.                 |

### Signals

n/a
