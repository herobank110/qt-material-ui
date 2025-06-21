# Menu

**Menus display a list of choices on a temporary surface**

## Usage

```python
from material_ui.menu import Menu, MenuItem

menu = Menu()

item1 = MenuItem()
item1.text = "Item 1"
item1.on_click.connect(lambda: print("Item 1 clicked"))
item1.setParent(menu)

item2 = MenuItem()
item2.text = "Item 2"
item2.on_click.connect(lambda: print("Item 2 clicked"))
item2.setParent(menu)

item3 = MenuItem()
item3.text = "Item 3"
item3.on_click.connect(lambda: print("Item 3 clicked"))
item3.setParent(menu)
```

## API

### Properties

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |

### Signals

| Name | Arguments | Description |
| ---- | --------- | ----------- |
