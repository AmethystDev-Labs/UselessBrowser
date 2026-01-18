from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer


class EdgeHighlightWidget(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        highlight_color: QtGui.QColor = None,
        highlight_width: int = 2,
        corner_radius: int = 12,
        animated: bool = True
    ):
        super().__init__(parent)
        self._highlight_color = highlight_color or QtGui.QColor(100, 149, 237, 200)
        self._highlight_width = highlight_width
        self._corner_radius = corner_radius
        self._animated = animated
        self._pulse_animation = QTimer(self)
        self._pulse_animation.timeout.connect(self._update_pulse)
        self._pulse_value = 0.0
        self._pulse_direction = 1
        self._pulse_speed = 0.02

        if self._animated:
            self._pulse_animation.start(16)

    def _update_pulse(self):
        self._pulse_value += self._pulse_speed * self._pulse_direction
        if self._pulse_value >= 1.0:
            self._pulse_value = 1.0
            self._pulse_direction = -1
        elif self._pulse_value <= 0.0:
            self._pulse_value = 0.0
            self._pulse_direction = 1
        self.update()

    def setHighlightColor(self, color: QtGui.QColor):
        self._highlight_color = color
        self.update()

    def setHighlightWidth(self, width: int):
        self._highlight_width = width
        self.update()

    def setCornerRadius(self, radius: int):
        self._corner_radius = radius
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        current_alpha = int(self._highlight_color.alpha() * (0.7 + 0.3 * self._pulse_value))
        highlight_color = QtGui.QColor(
            self._highlight_color.red(),
            self._highlight_color.green(),
            self._highlight_color.blue(),
            current_alpha
        )

        painter.setPen(QtGui.QPen(highlight_color, self._highlight_width))
        painter.setBrush(Qt.Brush.NoBrush)
        painter.drawRoundedRect(self.rect(), self._corner_radius, self._corner_radius)


class GlassEdgeHighlight(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        position: str = 'top',
        color: QtGui.QColor = None,
        width: int = 3
    ):
        super().__init__(parent)
        self._position = position
        self._color = color or QtGui.QColor(255, 255, 255, 150)
        self._width = width
        self._gradient_width = 30
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def setPosition(self, position: str):
        self._position = position
        self.update()

    def setColor(self, color: QtGui.QColor):
        self._color = color
        self.update()

    def setWidth(self, width: int):
        self._width = width
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        if self._position == 'top':
            gradient = QtGui.QLinearGradient(0, 0, 0, self._gradient_width)
            gradient.setColorAt(0, self._color)
            gradient.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
            painter.fillRect(0, 0, self.width(), self._gradient_width, gradient)
        elif self._position == 'bottom':
            gradient = QtGui.QLinearGradient(0, self.height() - self._gradient_width, 0, self.height())
            gradient.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
            gradient.setColorAt(1, self._color)
            painter.fillRect(0, self.height() - self._gradient_width, self.width(), self._gradient_width, gradient)
        elif self._position == 'left':
            gradient = QtGui.QLinearGradient(0, 0, self._gradient_width, 0)
            gradient.setColorAt(0, self._color)
            gradient.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
            painter.fillRect(0, 0, self._gradient_width, self.height(), gradient)
        elif self._position == 'right':
            gradient = QtGui.QLinearGradient(self.width() - self._gradient_width, 0, self.width(), 0)
            gradient.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
            gradient.setColorAt(1, self._color)
            painter.fillRect(self.width() - self._gradient_width, 0, self._gradient_width, self.height(), gradient)
        elif self._position == 'all':
            self._draw_all_edges(painter)


class GlowEffect(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        color: QtGui.QColor = None,
        radius: int = 50,
        intensity: float = 0.5
    ):
        super().__init__(parent)
        self._color = color or QtGui.QColor(100, 149, 237, 100)
        self._radius = radius
        self._intensity = intensity
        self._animation_timer = QTimer(self)
        self._animation_timer.timeout.connect(self._animate_glow)
        self._animation_phase = 0.0
        self._animation_timer.start(16)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _animate_glow(self):
        self._animation_phase += 0.05
        if self._animation_phase >= 6.28:
            self._animation_phase = 0.0
        self.update()

    def setColor(self, color: QtGui.QColor):
        self._color = color
        self.update()

    def setRadius(self, radius: int):
        self._radius = radius
        self.update()

    def setIntensity(self, intensity: float):
        self._intensity = intensity
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pulse = 0.8 + 0.2 * math.sin(self._animation_phase)
        current_intensity = self._intensity * pulse

        center = self.rect().center()
        glow = QtGui.QRadialGradient(center, self._radius)
        glow.setColorAt(0, QtGui.QColor(
            self._color.red(),
            self._color.green(),
            self._color.blue(),
            int(255 * current_intensity)
        ))
        glow.setColorAt(0.5, QtGui.QColor(
            self._color.red(),
            self._color.green(),
            self._color.blue(),
            int(100 * current_intensity)
        ))
        glow.setColorAt(1, QtGui.QColor(0, 0, 0, 0))

        painter.fillRect(self.rect(), glow)


class ReflectionEffect(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        color: QtGui.QColor = None,
        opacity: float = 0.3,
        length: float = 0.3
    ):
        super().__init__(parent)
        self._color = color or QtGui.QColor(255, 255, 255)
        self._opacity = opacity
        self._length = length
        self._offset = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate_reflection)
        self._timer.start(16)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _animate_reflection(self):
        self._offset -= 0.02
        if self._offset <= -1.0:
            self._offset = 0.0
        self.update()

    def setOpacity(self, opacity: float):
        self._opacity = opacity
        self.update()

    def setLength(self, length: float):
        self._length = length
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        height = int(self.height() * self._length)
        y_start = int(self.height() * (0.5 + self._offset * 0.5))

        gradient = QtGui.QLinearGradient(0, y_start - height, 0, y_start)
        gradient.setColorAt(0, QtGui.QColor(0, 0, 0, 0))
        gradient.setColorAt(0.5, QtGui.QColor(
            self._color.red(),
            self._color.green(),
            self._color.blue(),
            int(255 * self._opacity * 0.5)
        ))
        gradient.setColorAt(1, QtGui.QColor(
            self._color.red(),
            self._color.green(),
            self._color.blue(),
            int(255 * self._opacity)
        ))

        painter.fillRect(0, y_start - height, self.width(), height, gradient)


class SoftShadow(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        color: QtGui.QColor = None,
        blur_radius: int = 40,
        offset_x: int = 0,
        offset_y: int = 8
    ):
        super().__init__(parent)
        self._color = color or QtGui.QColor(0, 0, 0, 100)
        self._blur_radius = blur_radius
        self._offset_x = offset_x
        self._offset_y = offset_y
        self._opacity = 1.0

        self._shadow_pixmap = None
        self._update_shadow_pixmap()

    def _update_shadow_pixmap(self):
        size = max(self.width(), self.height()) + self._blur_radius * 2
        self._shadow_pixmap = QtGui.QPixmap(size, size)
        self._shadow_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(self._shadow_pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        center = size // 2
        gradient = QtGui.QRadialGradient(center, self._blur_radius)
        gradient.setColorAt(0, QtGui.QColor(
            self._color.red(),
            self._color.green(),
            self._color.blue(),
            int(255 * self._opacity)
        ))
        gradient.setColorAt(1, QtGui.QColor(0, 0, 0, 0))

        painter.fillRect(self.rect(), gradient)
        painter.end()

    def setColor(self, color: QtGui.QColor):
        self._color = color
        self._update_shadow_pixmap()
        self.update()

    def setBlurRadius(self, radius: int):
        self._blur_radius = radius
        self._update_shadow_pixmap()
        self.update()

    def setOffset(self, x: int, y: int):
        self._offset_x = x
        self._offset_y = y
        self.update()

    def paintEvent(self, event):
        if self._shadow_pixmap:
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
            x = (self.width() - self._shadow_pixmap.width()) // 2 + self._offset_x
            y = (self.height() - self._shadow_pixmap.height()) // 2 + self._offset_y
            painter.drawPixmap(int(x), int(y), self._shadow_pixmap)


class AnimatedBorder(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        color: QtGui.QColor = None,
        width: int = 2,
        corner_radius: int = 12,
        direction: str = 'clockwise'
    ):
        super().__init__(parent)
        self._color = color or QtGui.QColor(100, 149, 237)
        self._width = width
        self._corner_radius = corner_radius
        self._direction = 1 if direction == 'clockwise' else -1
        self._offset = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate_border)
        self._timer.start(16)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _animate_border(self):
        self._offset += 0.02 * self._direction
        if self._offset >= 1.0:
            self._offset = 0.0
        self.update()

    def setColor(self, color: QtGui.QColor):
        self._color = color
        self.update()

    def setWidth(self, width: int):
        self._width = width
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(self._width // 2, self._width // 2, -self._width // 2, -self._width // 2)

        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, self._corner_radius, self._corner_radius)

        gradient = QtGui.QLinearGradient(rect.topLeft(), rect.bottomRight())
        stops = [0.0, 0.25, 0.5, 0.75, 1.0]
        for i, stop in enumerate(stops):
            hue = (self._offset + stop) % 1.0
            color = QtGui.QColor.fromHsvF(hue, 0.7, 0.9)
            gradient.setColorAt(stop, color)

        painter.setPen(QtGui.QPen(gradient, self._width))
        painter.setBrush(Qt.Brush.NoBrush)
        painter.drawPath(path)


def apply_soft_shadow(widget: QtWidgets.QWidget, color: QtGui.QColor = None, blur: int = 30, offset: tuple = (0, 4)):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setColor(color or QtGui.QColor(0, 0, 0, 80))
    shadow.setBlurRadius(blur)
    shadow.setOffset(offset[0], offset[1])
    widget.setGraphicsEffect(shadow)


def add_edge_glow(widget: QtWidgets.QWidget, color: QtGui.QColor = None, positions: list = ['top']):
    for position in positions:
        glow = GlassEdgeHighlight(widget, position, color)
        if position == 'top':
            glow.setFixedHeight(3)
            glow.setGeometry(0, 0, widget.width(), 3)
        elif position == 'bottom':
            glow.setFixedHeight(3)
            glow.setGeometry(0, widget.height() - 3, widget.width(), 3)
        elif position == 'left':
            glow.setFixedWidth(3)
            glow.setGeometry(0, 0, 3, widget.height())
        elif position == 'right':
            glow.setFixedWidth(3)
            glow.setGeometry(widget.width() - 3, 0, 3, widget.height())
