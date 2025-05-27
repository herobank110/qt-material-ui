# Icons

**Icons are small symbols to easily identify actions and categories.**

![demonstration](./icons.jpg)

## Usage

```python
from material_ui.icon import Icon

icon = Icon()
icon.icon_name = "star"
```

## Icon Font

The icon font used is
[Material Symbols](https://fonts.google.com/icons). You can find the
available icons and their names on the Google Fonts website.

Variable axes are used to control the style of the icon.

## API

### Properties

| Name                | Type                      | Default      | Description                                                           |
| ------------------- | ------------------------- | ------------ | --------------------------------------------------------------------- |
| `selected`          | `bool`                    | `False`      | Whether the checkbox is checked.                                      |
| `icon_name`         | `str`                     | `"star"`     | Icon name to display. See: https://fonts.google.com/icons.            |
| `icon_style`        | `IconStyle`               | `"outlined"` | Icon style. Either 'outlined', 'rounded', or 'sharp'.                 |
| `font_size`         | `DesignToken` \| `int`    | `24`         | Font size of icon.                                                    |
| `color `            | `DesignToken` \| `QColor` | `on_surface` | Color of the icon.                                                    |
| `weight`            | `int`                     | `400`        | Main control of thickness. 400 is default, 100 is thin, 700 is thick. |
| `filled `           | `bool`                    | `False`      | Whether the icon should be filled.                                    |
| `grade`             | `int`                     | `0`          | Thickness. 0 is default, -25 is thin, 200 is thick.                   |
| `use_optical_size ` | `bool`                    | `True`       | Whether to set the optical size to match the font size.               |

### Signals

n/a
