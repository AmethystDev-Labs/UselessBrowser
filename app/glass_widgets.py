from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, pyqtProperty
from PyQt6.QtWidgets import QGraphicsBlurEffect, QGraphicsDropShadowEffect
import math


class GlassCardWidget(QtWidgets.QFrame):
    def __init__(
        self,
        parent=None,
        blur_radius: float = 20.0,
        opacity: float = 0.85,
        corner_radius: int = 16
    ):
        super().__init__(parent)
        self._blur_radius = blur_radius
        self._opacity = opacity
        self._corner_radius = corner_radius
        self._border_color = QtGui.QColor(255, 255, 255, 40)
        self._border_width = 1

        self._setup_ui()
        self._setup_effects()

    def _setup_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background: transparent;')
        self.setContentsMargins(16, 16, 16, 16)

    def _setup_effects(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QtGui.QColor(0, 0, 0, 50))
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

    @pyqtProperty(float)
    def blurRadius(self) -> float:
        return self._blur_radius

    @blurRadius.setter
    def blurRadius(self, value: float):
        self._blur_radius = value
        self.update()

    def setBlurRadius(self, radius: float):
        self._blur_radius = radius
        self.update()

    def setCornerRadius(self, radius: int):
        self._corner_radius = radius
        self.update()

    def setBorderColor(self, color: QtGui.QColor):
        self._border_color = color
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()

        painter.save()
        path = QtGui.QPainterPath()
        path.addRoundedRect(
            self._border_width,
            self._border_width,
            rect.width() - self._border_width * 2,
            rect.height() - self._border_width * 2,
            self._corner_radius,
            self._corner_radius
        )
        painter.setClipPath(path)

        gradient = QtGui.QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, QtGui.QColor(255, 255, 255, int(25 * self._opacity)))
        gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, int(15 * self._opacity)))
        gradient.setColorAt(1, QtGui.QColor(255, 255, 255, int(5 * self._opacity)))
        painter.fillRect(rect, gradient)

        painter.restore()

        if self._border_width > 0:
            painter.setPen(QtGui.QPen(self._border_color, self._border_width))
            painter.setBrush(Qt.Brush.NoBrush)
            painter.drawRoundedRect(
                self._border_width,
                self._border_width,
                rect.width() - self._border_width * 2,
                rect.height() - self._border_width * 2,
                self._corner_radius,
                self._corner_radius
            )


class GlassContainer(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        corner_radius: int = 16
    ):
        super().__init__(parent)
        self._corner_radius = corner_radius
        self._border_color = QtGui.QColor(255, 255, 255, 30)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background: transparent;')

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QtGui.QColor(0, 0, 0, 40))
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def setCornerRadius(self, radius: int):
        self._corner_radius = radius
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(QtGui.QPen(self._border_color, 1))
        painter.setBrush(Qt.Brush.NoBrush)
        painter.drawRoundedRect(self.rect(), self._corner_radius, self._corner_radius)


class GlassButton(QtWidgets.QPushButton):
    def __init__(
        self,
        text: str,
        parent=None,
        primary: bool = True,
        corner_radius: int = 10
    ):
        super().__init__(text, parent)
        self._primary = primary
        self._corner_radius = corner_radius
        self._hover_progress = 0.0

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet('background: transparent;')
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(40)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QtGui.QColor(0, 0, 0, 30))
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def enterEvent(self, event):
        self._hover_progress = 1.0
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_progress = 0.0
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()

        if self._primary:
            base_color = QtGui.QColor(70, 130, 200)
            hover_color = QtGui.QColor(100, 160, 230)
        else:
            base_color = QtGui.QColor(255, 255, 255, 40)
            hover_color = QtGui.QColor(255, 255, 255, 70)

        current_color = QtGui.QColor(
            int(base_color.red() + (hover_color.red() - base_color.red()) * self._hover_progress),
            int(base_color.green() + (hover_color.green() - base_color.green()) * self._hover_progress),
            int(base_color.blue() + (hover_color.blue() - base_color.blue()) * self._hover_progress),
            int(base_color.alpha() + (hover_color.alpha() - base_color.alpha()) * self._hover_progress)
        )

        painter.setBrush(QtGui.QBrush(current_color))
        painter.drawRoundedRect(rect, self._corner_radius, self._corner_radius)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())


def apply_glass_style(widget: QtWidgets.QWidget, blur_radius: float = 15.0, opacity: float = 0.8):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setColor(QtGui.QColor(0, 0, 0, 50))
    shadow.setBlurRadius(20)
    shadow.setOffset(0, 4)
    widget.setGraphicsEffect(shadow)

    widget.setStyleSheet(f'''
        background-color: rgba(40, 40, 65, {int(opacity * 255)};
        border: 1px solid rgba(255, 255, 255, 35);
        border-radius: 16px;
        background: transparent;
    ''')
