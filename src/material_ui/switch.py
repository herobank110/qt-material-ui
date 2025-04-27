from qtpy import QtCore, QtGui, QtWidgets
from material_ui._component import Component, Signal, effect, use_state

md_comp_switch_unselected_track_outline_color = "#79747E"
md_comp_switch_unselected_track_color = "#E6E0E9"
md_comp_switch_selected_track_color = "#6750A4"
md_comp_switch_selected_handle_color = "#FFFFFF"


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    selected = use_state(False)

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(52, 32)

        graphics_scene = QtWidgets.QGraphicsScene()
        graphics_scene.setSceneRect(self.rect())
        handle = graphics_scene.addEllipse(
            QtCore.QRect(),
            QtCore.Qt.NoPen,
            QtGui.QBrush(md_comp_switch_selected_handle_color),
        )
        handle.setRect(QtCore.QRect(0, 0, 16, 16))
        handle.setPos(QtCore.QPoint(4, (32 - 16) / 2 - 4))

        handle.setRect(QtCore.QRect(0, 0, 28, 28))
        handle.setPos(QtCore.QPoint(52 - 28 - 2, 2))

        graphics_view = QtWidgets.QGraphicsView()
        graphics_view.setRenderHint(QtGui.QPainter.Antialiasing)
        graphics_view.setParent(self)
        graphics_view.setStyleSheet(
            "background:transparent;border:none;border-radius:none;"
        )
        # graphics_view.move(0, 0)
        # graphics_view.resize(50, 50)
        graphics_view.setScene(graphics_scene)
        graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if event.button() == QtCore.Qt.LeftButton:
            # Toggle the checked state
            self.selected.set(not self.selected.get())
        return super().mousePressEvent(event)

    @effect(selected)
    def _apply_style(self) -> None:
        """Apply the style based on the selected state."""
        if not self.selected.get():
            # unselected
            style = {
                "background-color": md_comp_switch_unselected_track_color,
                "border": f"2px solid {md_comp_switch_unselected_track_outline_color}",
            }
        else:
            # selected
            style = {
                "background-color": md_comp_switch_selected_track_color,
                "border": "none",
            }

        style.update(
            {
                "border-radius": "16px",
            }
        )
        self.sx.set(style)
