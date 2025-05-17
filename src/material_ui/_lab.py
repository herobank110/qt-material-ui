"""Experimental file for figuring things out."""

from material_ui.tokens import DesignToken, resolve_token
from qtpy.QtWidgets import QGraphicsDropShadowEffect
from qtpy.QtGui import QColor
from qtpy.QtCore import QPropertyAnimation, QPointF
from material_ui.tokens import md_sys_elevation, md_sys_color
from material_ui.tokens._utils import find_root_token

_ELEVATION_BLUR_RADIUS_MAP: dict[DesignToken, int] = {
    md_sys_elevation.level0: 0,
    md_sys_elevation.level1: 3,
    md_sys_elevation.level2: 6,
    md_sys_elevation.level3: 8,
    md_sys_elevation.level4: 10,
    # TODO: implement token generator overrides for missing tokens
    # md_sys_elevation.level5: 4,
}

_ELEVATION_OFFSET_MAP: dict[DesignToken, QPointF] = {
    md_sys_elevation.level0: QPointF(0.0, 0.0),
    md_sys_elevation.level1: QPointF(0.0, 1.0),
    md_sys_elevation.level2: QPointF(0.0, 2.0),
    md_sys_elevation.level3: QPointF(0.0, 4.0),
    md_sys_elevation.level4: QPointF(0.0, 6.0),
    # md_sys_elevation.level5: QPointF(0, 4),
}


class DropShadow(QGraphicsDropShadowEffect):
    """Drop shadow supporting Material design tokens.

    TODO:
      transition for elevation
      2 shadows per elevation level - key and ambient
        see: https://github.com/material-components/material-web/blob/main/elevation/internal/_elevation.scss#L63
    """

    def __init__(self) -> None:
        super().__init__()

        self._elevation = md_sys_elevation.level0
        self._shadow_color = md_sys_color.shadow
        self._apply_elevation()

    @property
    def elevation(self) -> DesignToken:
        """Get the elevation value."""
        return self._elevation

    @elevation.setter
    def elevation(self, value: DesignToken) -> None:
        """Set the elevation value."""
        if self._elevation == value:
            return
        self._elevation = value
        self._apply_elevation()

    def _apply_elevation(self) -> None:
        self.setBlurRadius(self._get_computed_blur_radius())
        self.setOffset(self._get_computed_offset())
        # self.setBlurRadius(0)
        # self.setOffset(1, 1)

    def _get_computed_blur_radius(self) -> int:
        return _ELEVATION_BLUR_RADIUS_MAP[find_root_token(self._elevation)]

    def _get_computed_offset(self) -> QPointF:
        return _ELEVATION_OFFSET_MAP[find_root_token(self._elevation)]

    def animate_elevation_to(self, value: DesignToken) -> None:
        """Animate the elevation to a new value."""
        self._elevation = value

        blur_radius_animation = QPropertyAnimation()
        blur_radius_animation.setParent(self)
        blur_radius_animation.setTargetObject(self)
        blur_radius_animation.setPropertyName(b"blurRadius")
        blur_radius_animation.setEndValue(self._get_computed_blur_radius())
        blur_radius_animation.setDuration(120)
        # blur_radius_animation.setEasingCurve(QEasingCurve.InCubic)
        blur_radius_animation.start()

        offset_animation = QPropertyAnimation()
        offset_animation.setParent(self)
        offset_animation.setTargetObject(self)
        offset_animation.setPropertyName(b"offset")
        offset_animation.setEndValue(self._get_computed_offset())
        offset_animation.setDuration(120)
        # offset_animation.setEasingCurve(QEasingCurve.InCubic)
        offset_animation.start()

    @property
    def shadow_color(self) -> DesignToken:
        """Get the shadow color value."""
        return self._shadow_color

    @shadow_color.setter
    def shadow_color(self, value: DesignToken) -> None:
        """Set the shadow color value."""
        if self._shadow_color == value:
            return
        self._shadow_color = value

        resolved_color = resolve_token(self._shadow_color)
        if not isinstance(resolved_color, QColor):
            raise RuntimeError(
                f"Unexpected shadow_color token value (expected QColor, got "
                f"{type(resolved_color).__name__})"
            )
        resolved_color.setAlphaF(0.6)
        self.setColor(resolved_color)
        # self.setColor(QColor("rgba(0, 244, 0, 70)"))


# Testing for a multi shadow effect based on CSS
# also focus indicator outside widget bounds?
from qtpy.QtGui import QPainter, QTransform
from qtpy.QtWidgets import QGraphicsEffect
from qtpy.QtCore import QRectF

X = 2


class MyGraphicsEffect(QGraphicsEffect):
    """Testing Effect."""

    def boundingRectFor(self, rect: QRectF) -> QRectF:
        """Override the bounding rectangle to add extra padding."""
        return rect.adjusted(-X, -X, X, X)

    def draw(self, painter: QPainter) -> None:
        """Override the draw method to add custom drawing."""
        # return
        # self.drawSource(painter)
        # return
        # if not painter.isActive():
        #     return
        #     painter.begin(painter.device())
        dpr = painter.device().devicePixelRatioF()
        # painter.save()
        print(dpr)
        # painter.scale(1/dpr, 1/dpr)
        # original_transform = painter.worldTransform()
        # painter.setWorldTransform(QTransform())
        painter.setBrush(QColor(255, 0, 0, 50))
        painter.drawRect(self.boundingRect().adjusted(-X, -X, X, X))
        # painter.drawRect(self.boundingRect().adjusted(-X*dpr, -X*dpr, X*dpr, X*dpr))
        # painter.restore()
        # from qtpy.QtGui import QTransform
        # painter.setTransform(QTransform())
        self.drawSource(painter)
        # painter.setWorldTransform(original_transform)


from qtpy.QtWidgets import QApplication, QWidget


def test_graphics_effect():
    app = QApplication()
    window = QWidget()
    window.setStyleSheet("background-color:white;")
    window.resize(200, 200)
    widget = QWidget(window)
    widget.setGeometry(50, 50, 100, 100)
    widget.setStyleSheet("background-color:lightblue;border-radius:10px;")
    effect = MyGraphicsEffect()
    widget.setGraphicsEffect(effect)
    window.show()
    app.exec_()


def test_icon_font():
    app = QApplication()

    import httpx
    import tempfile
    from pathlib import Path

    font_file = (
        Path(tempfile.gettempdir()) / "MaterialSymbolsOutlined[FILL,GRAD,opsz,wght].ttf"
    )
    if not font_file.exists():
        resp = httpx.get(
            "https://raw.githubusercontent.com/google/material-design-icons/refs/heads/master/variablefont/MaterialSymbolsOutlined[FILL,GRAD,opsz,wght].ttf"
        )
        with open(font_file, "wb") as f:
            f.write(resp.content)

    from qtpy.QtGui import QFontDatabase, QFont

    font_id = QFontDatabase.addApplicationFont(str(font_file))
    family = QFontDatabase.applicationFontFamilies(font_id)
    print(family)
    # font = QFontDatabase.font(family[0], "100", 12)
    font = QFont("Material Symbols Outlined", pointSize=24, weight=400)
    # font.setVariableAxis(QFont.Tag("FILL"), 1)
    font.setVariableAxis(QFont.Tag("GRAD"), 200)
    # font.variableAxisTags()
    # font.setStyleHint()
    from qtpy.QtWidgets import QLabel
    label = QLabel("home")
    label.setFont(font)
    # label.font().setStyleStrategy(QFont.PreferAntialias)
    label.setStyleSheet("background-color:blue;color:green;")
    label.show()

    app.exec()


if __name__ == "__main__":
    # test_graphics_effect()
    test_icon_font()
