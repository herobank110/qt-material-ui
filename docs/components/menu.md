# Menu

**Menus display a list of choices on a temporary surface**

## Usage

```python
from material_ui.menu import Menu, MenuItem

menu = Menu()

item1 = MenuItem()
item1.text = "Item 1"
item1.on_click.connect(lambda: print("Item 1 clicked"))
menu.add_widget(item1)

item2 = MenuItem()
item2.text = "Item 2"
item2.on_click.connect(lambda: print("Item 2 clicked"))
menu.add_widget(item2)

item3 = MenuItem()
item3.text = "Item 3"
item3.on_click.connect(lambda: print("Item 3 clicked"))
menu.add_widget(item3)
```

## API

### Properties

| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |

### Signals

| Name | Arguments | Description |
| ---- | --------- | ----------- |
