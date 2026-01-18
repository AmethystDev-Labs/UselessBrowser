from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer
import math


class GlassBackground(QtWidgets.QWidget):
    def __init__(self, parent=None, theme: str = 'dark'):
        super().__init__(parent)
        self._theme = theme
        self._time = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_time)
        self._timer.start(16)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAutoFillBackground(False)

    def _update_time(self):
        self._time += 0.016
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        w, h = self.width(), self.height()

        if w <= 0 or h <= 0:
            return

        if self._theme == 'dark':
            self._paint_dark_background(painter, w, h)
        else:
            self._paint_light_background(painter, w, h)

    def _paint_dark_background(self, painter: QtGui.QPainter, w: int, h: int):
        gradient1 = QtGui.QRadialGradient(w * 0.2, h * 0.3, max(w, h) * 0.6)
        gradient1.setColorAt(0, QtGui.QColor(45, 45, 70))
        gradient1.setColorAt(0.7, QtGui.QColor(25, 25, 45))
        gradient1.setColorAt(1, QtGui.QColor(15, 15, 30))
        painter.fillRect(0, 0, w, h, gradient1)

        gradient2 = QtGui.QRadialGradient(
            w * (0.5 + 0.2 * math.sin(self._time * 0.3)),
            h * (0.5 + 0.1 * math.cos(self._time * 0.2)),
            max(w, h) * 0.4
        )
        gradient2.setColorAt(0, QtGui.QColor(70, 60, 120, 80))
        gradient2.setColorAt(0.5, QtGui.QColor(60, 50, 100, 50))
        gradient2.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, w, h, gradient2)

        gradient3 = QtGui.QRadialGradient(
            w * (0.8 + 0.1 * math.cos(self._time * 0.25)),
            h * (0.7 + 0.15 * math.sin(self._time * 0.35)),
            max(w, h) * 0.35
        )
        gradient3.setColorAt(0, QtGui.QColor(40, 80, 130, 60))
        gradient3.setColorAt(0.5, QtGui.QColor(35, 70, 110, 40))
        gradient3.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, w, h, gradient3)

    def _paint_light_background(self, painter: QtGui.QPainter, w: int, h: int):
        gradient1 = QtGui.QRadialGradient(w * 0.5, h * 0.5, max(w, h) * 0.7)
        gradient1.setColorAt(0, QtGui.QColor(250, 250, 255))
        gradient1.setColorAt(0.7, QtGui.QColor(240, 242, 250))
        gradient1.setColorAt(1, QtGui.QColor(230, 235, 245))
        painter.fillRect(0, 0, w, h, gradient1)

        gradient2 = QtGui.QRadialGradient(
            w * (0.3 + 0.2 * math.sin(self._time * 0.3)),
            h * (0.4 + 0.1 * math.cos(self._time * 0.25)),
            max(w, h) * 0.4
        )
        gradient2.setColorAt(0, QtGui.QColor(200, 210, 255, 60))
        gradient2.setColorAt(0.5, QtGui.QColor(180, 200, 245, 40))
        gradient2.setColorAt(1, QtGui.QColor(0, 0, 0, 0))
        painter.fillRect(0, 0, w, h, gradient2)

    def set_theme(self, theme: str):
        self._theme = theme
        self.update()
