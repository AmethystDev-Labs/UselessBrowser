from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QGraphicsBlurEffect, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty


class FrostedGlassWidget(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        blur_radius: float = 15.0,
        opacity: float = 0.7,
        color: QtGui.QColor = None
    ):
        super().__init__(parent)
        self._blur_radius = blur_radius
        self._opacity = opacity
        self._color = color or QtGui.QColor(255, 255, 255, 40)
        self._border_color = QtGui.QColor(255, 255, 255, 50)
        self._border_width = 1
        self._corner_radius = 16
        self._shadow_enabled = True
        self._shadow_color = QtGui.QColor(0, 0, 0, 80)
        self._shadow_blur = 30
        self._shadow_offset = QtCore.QPointF(0, 4)

        self._setup_effects()
        self._setup_animations()

    def _setup_effects(self):
        self._blur_effect = QGraphicsBlurEffect(self)
        self._blur_effect.setBlurRadius(self._blur_radius)
        self._blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.PerformanceHint)
        self.setGraphicsEffect(self._blur_effect)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(self._opacity)
        self.setGraphicsEffect(self._opacity_effect)

        if self._shadow_enabled:
            self._shadow_effect = QGraphicsDropShadowEffect(self)
            self._shadow_effect.setColor(self._shadow_color)
            self._shadow_effect.setBlurRadius(self._shadow_blur)
            self._shadow_effect.setOffset(self._shadow_offset)
            self.setGraphicsEffect(self._shadow_effect)

    def _setup_animations(self):
        self._blur_animation = QPropertyAnimation(self, b"blurRadius")
        self._blur_animation.setDuration(300)
        self._blur_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._opacity_animation = QPropertyAnimation(self, b"glassOpacity")
        self._opacity_animation.setDuration(300)
        self._opacity_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(float)
    def blurRadius(self) -> float:
        return self._blur_radius

    @blurRadius.setter
    def blurRadius(self, value: float):
        self._blur_radius = value
        self._blur_effect.setBlurRadius(value)

    @pyqtProperty(float)
    def glassOpacity(self) -> float:
        return self._opacity

    @glassOpacity.setter
    def glassOpacity(self, value: float):
        self._opacity = value
        self._opacity_effect.setOpacity(value)

    def setBlurRadius(self, radius: float):
        self._blur_animation.setStartValue(self._blur_radius)
        self._blur_animation.setEndValue(radius)
        self._blur_animation.start()

    def setGlassOpacity(self, opacity: float):
        self._opacity_animation.setStartValue(self._opacity)
        self._opacity_animation.setEndValue(opacity)
        self._opacity_animation.start()

    def setCornerRadius(self, radius: int):
        self._corner_radius = radius
        self.update()

    def setBorderColor(self, color: QtGui.QColor):
        self._border_color = color
        self.update()

    def setBorderWidth(self, width: int):
        self._border_width = width
        self.update()

    def enterEvent(self, event):
        self.setBlurRadius(max(5.0, self._blur_radius - 5))
        self.setGlassOpacity(min(0.95, self._opacity + 0.05))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setBlurRadius(self._blur_radius)
        self.setGlassOpacity(self._opacity)
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            self._border_width / 2,
            self._border_width / 2,
            self.width() - self._border_width,
            self.height() - self._border_width,
            self._corner_radius,
            self._corner_radius
        )
        painter.setClipPath(path)

        painter.fillRect(self.rect(), self._color)

        if self._border_width > 0:
            painter.setPen(QtGui.QPen(self._border_color, self._border_width))
            painter.setBrush(Qt.Brush.NoBrush)
            painter.drawRoundedRect(
                self._border_width / 2,
                self._border_width / 2,
                self.width() - self._border_width,
                self.height() - self._border_width,
                self._corner_radius,
                self._corner_radius
            )


class GlassCard(QtWidgets.QFrame):
    def __init__(
        self,
        parent=None,
        blur_radius: float = 20.0,
        opacity: float = 0.75,
        color: QtGui.QColor = None
    ):
        super().__init__(parent)
        self._blur_radius = blur_radius
        self._opacity = opacity
        self._color = color or QtGui.QColor(40, 40, 60, 200)

        self._setup_ui()
        self._setup_effects()

    def _setup_ui(self):
        self.setFixedHeight(120)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.setStyleSheet("""
            GlassCard {
                background: transparent;
                border: none;
            }
        """)

    def _setup_effects(self):
        self._blur_effect = QGraphicsBlurEffect(self)
        self._blur_effect.setBlurRadius(self._blur_radius)
        self._blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.QualityHint)
        self.setGraphicsEffect(self._blur_effect)

        self._shadow_effect = QGraphicsDropShadowEffect(self)
        self._shadow_effect.setColor(QtGui.QColor(0, 0, 0, 60))
        self._shadow_effect.setBlurRadius(25)
        self._shadow_effect.setOffset(0, 8)
        self.setGraphicsEffect(self._shadow_effect)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 30), 1))
        painter.setBrush(QtGui.QBrush(self._color))
        painter.drawRoundedRect(self.rect(), 20, 20)

        gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QtGui.QColor(255, 255, 255, 20))
        gradient.setColorAt(0.5, QtGui.QColor(255, 255, 255, 5))
        gradient.setColorAt(1, QtGui.QColor(255, 255, 255, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QtGui.QBrush(gradient))
        painter.drawRoundedRect(self.rect(), 20, 20)


class GlassPanel(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        blur_radius: float = 12.0,
        opacity: float = 0.8
    ):
        super().__init__(parent)
        self._blur_radius = blur_radius
        self._opacity = opacity
        self._corner_radius = 12
        self._border_color = QtGui.QColor(255, 255, 255, 25)
        self._fill_color = QtGui.QColor(35, 35, 55, 220)

        self._setup_effects()

    def _setup_effects(self):
        self._blur_effect = QGraphicsBlurEffect(self)
        self._blur_effect.setBlurRadius(self._blur_radius)
        self._blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.PerformanceHint)
        self.setGraphicsEffect(self._blur_effect)

        self._opacity_effect = QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(self._opacity)
        self.setGraphicsEffect(self._opacity_effect)

    def setCornerRadius(self, radius: int):
        self._corner_radius = radius
        self.update()

    def setFillColor(self, color: QtGui.QColor):
        self._fill_color = color
        self.update()

    def setBorderColor(self, color: QtGui.QColor):
        self._border_color = color
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        painter.setPen(QtGui.QPen(self._border_color, 1))
        painter.setBrush(QtGui.QBrush(self._fill_color))
        painter.drawRoundedRect(rect, self._corner_radius, self._corner_radius)


class GlassButton(QtWidgets.QPushButton):
    def __init__(
        self,
        text: str,
        parent=None,
        primary: bool = True,
        blur_radius: float = 8.0
    ):
        super().__init__(text, parent)
        self._primary = primary
        self._blur_radius = blur_radius
        self._corner_radius = 10
        self._hover_animation = QPropertyAnimation(self, b"animationProgress")
        self._hover_animation.setDuration(200)
        self._hover_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._animation_progress = 0.0

        self._setup_style()
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setup_style(self):
        if self._primary:
            self._normal_color = QtGui.QColor(100, 149, 237, 200)
            self._hover_color = QtGui.QColor(120, 169, 255, 230)
            self._text_color = QtGui.QColor(255, 255, 255)
        else:
            self._normal_color = QtGui.QColor(255, 255, 255, 40)
            self._hover_color = QtGui.QColor(255, 255, 255, 70)
            self._text_color = QtGui.QColor(255, 255, 255)

    @pyqtProperty(float)
    def animationProgress(self) -> float:
        return self._animation_progress

    @animationProgress.setter
    def animationProgress(self, value: float):
        self._animation_progress = value
        self.update()

    def enterEvent(self, event):
        self._hover_animation.setStartValue(self._animation_progress)
        self._hover_animation.setEndValue(1.0)
        self._hover_animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover_animation.setStartValue(self._animation_progress)
        self._hover_animation.setEndValue(0.0)
        self._hover_animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        current_color = QtGui.QColor(
            int(self._normal_color.red() + (self._hover_color.red() - self._normal_color.red()) * self._animation_progress),
            int(self._normal_color.green() + (self._hover_color.green() - self._normal_color.green()) * self._animation_progress),
            int(self._normal_color.blue() + (self._hover_color.blue() - self._normal_color.blue()) * self._animation_progress),
            int(self._normal_color.alpha() + (self._hover_color.alpha() - self._normal_color.alpha()) * self._animation_progress)
        )

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 80), 1))
        painter.setBrush(QtGui.QBrush(current_color))
        painter.drawRoundedRect(self.rect(), self._corner_radius, self._corner_radius)

        painter.setPen(QtGui.QPen(self._text_color))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())


class GlassContainer(QtWidgets.QWidget):
    def __init__(
        self,
        parent=None,
        blur_radius: float = 10.0,
        opacity: float = 0.85
    ):
        super().__init__(parent)
        self._blur_radius = blur_radius
        self._opacity = opacity
        self._corner_radius = 16
        self._border_color = QtGui.QColor(255, 255, 255, 35)
        self._fill_color = QtGui.QColor(30, 30, 50, 230)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(16, 16, 16, 16)
        self._layout.setSpacing(12)

        self._setup_effects()

    def _setup_effects(self):
        self._blur_effect = QGraphicsBlurEffect(self)
        self._blur_effect.setBlurRadius(self._blur_radius)
        self._blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.QualityHint)
        self.setGraphicsEffect(self._blur_effect)

    def addWidget(self, widget: QtWidgets.QWidget):
        self._layout.addWidget(widget)

    def setCornerRadius(self, radius: int):
        self._corner_radius = radius
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        painter.setPen(QtGui.QPen(self._border_color, 1))
        painter.setBrush(QtGui.QBrush(self._fill_color))
        painter.drawRoundedRect(self.rect(), self._corner_radius, self._corner_radius)


def apply_frosted_glass(
    widget: QtWidgets.QWidget,
    blur_radius: float = 15.0,
    opacity: float = 0.8,
    color: QtGui.QColor = None
):
    blur_effect = QGraphicsBlurEffect(widget)
    blur_effect.setBlurRadius(blur_radius)
    blur_effect.setBlurHints(QGraphicsBlurEffect.BlurHint.QualityHint)
    widget.setGraphicsEffect(blur_effect)

    opacity_effect = QGraphicsOpacityEffect(widget)
    opacity_effect.setOpacity(opacity)
    widget.setGraphicsEffect(opacity_effect)
