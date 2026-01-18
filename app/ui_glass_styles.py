from PyQt6.QtCore import QFile, QTextStream
from app.app_config import resolve_theme_mode
from qfluentwidgets.common import Theme

GLASS_DARK_STYLESHEET = """
/* Frosted Glass Dark Theme */

QMainWindow {
    background: transparent;
}

QWidget {
    color: #ffffff;
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

/* Glass Window Background */
FluentWindow > QWidget#qt_central_widget {
    background: transparent;
}

/* Glass Cards - Semi-transparent with blur effect simulation */
SimpleCardWidget, CardWidget {
    background-color: rgba(30, 30, 40, 180);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 16px;
    padding: 16px;
}

/* Glass Card Hover Effect */
SimpleCardWidget:hover, CardWidget:hover {
    background-color: rgba(40, 40, 55, 200);
    border: 1px solid rgba(255, 255, 255, 50);
}

/* Navigation Pane - Glass Effect */
QFrame#navigationWidget {
    background-color: rgba(20, 20, 30, 150);
    border: none;
    border-right: 1px solid rgba(255, 255, 255, 20);
}

/* Navigation Items */
QPushButton[navButton="true"] {
    background-color: rgba(255, 255, 255, 10);
    border: 1px solid rgba(255, 255, 255, 15);
    border-radius: 8px;
    padding: 8px 12px;
    text-align: left;
    color: #ffffff;
}

QPushButton[navButton="true"]:hover {
    background-color: rgba(255, 255, 255, 20);
    border: 1px solid rgba(255, 255, 255, 40);
}

QPushButton[navButton="true"]:checked {
    background-color: rgba(100, 149, 237, 100);
    border: 1px solid rgba(100, 149, 237, 150);
}

/* Glass Buttons */
PrimaryPushButton, PushButton {
    background-color: rgba(100, 149, 237, 200);
    border: 1px solid rgba(100, 149, 237, 150);
    border-radius: 8px;
    padding: 8px 20px;
    color: #ffffff;
    font-weight: 500;
}

PrimaryPushButton:hover, PushButton:hover {
    background-color: rgba(120, 169, 255, 220);
    border: 1px solid rgba(120, 169, 255, 200);
}

PrimaryPushButton:pressed, PushButton:pressed {
    background-color: rgba(80, 129, 207, 200);
}

PushButton {
    background-color: rgba(255, 255, 255, 30);
    border: 1px solid rgba(255, 255, 255, 40);
}

PushButton:hover {
    background-color: rgba(255, 255, 255, 50);
}

/* Glass Input Fields */
LineEdit, ComboBox {
    background-color: rgba(0, 0, 0, 100);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 8px;
    padding: 10px 12px;
    color: #ffffff;
    selection-background-color: rgba(100, 149, 237, 150);
}

LineEdit:focus, ComboBox:focus {
    border: 1px solid rgba(100, 149, 237, 180);
    background-color: rgba(0, 0, 0, 80);
}

LineEdit::placeholder, ComboBox::placeholder {
    color: rgba(255, 255, 255, 100);
}

/* ComboBox Dropdown */
QComboBox QAbstractItemView {
    background-color: rgba(40, 40, 50, 230);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 8px;
    selection-background-color: rgba(100, 149, 237, 150);
    color: #ffffff;
}

/* Glass List Widget */
ListWidget {
    background-color: rgba(0, 0, 0, 50);
    border: 1px solid rgba(255, 255, 255, 20);
    border-radius: 12px;
    padding: 8px;
    color: #ffffff;
}

ListWidget::item {
    background-color: rgba(255, 255, 255, 10);
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 10px 12px;
    margin: 2px 0;
}

ListWidget::item:selected {
    background-color: rgba(100, 149, 237, 120);
    border: 1px solid rgba(100, 149, 237, 150);
}

ListWidget::item:hover {
    background-color: rgba(255, 255, 255, 20);
}

/* Glass Scroll Area */
ScrollArea {
    background: transparent;
    border: none;
}

ScrollArea > QWidget > QWidget {
    background: transparent;
}

/* Glass Scrollbars */
QScrollBar:vertical {
    background: rgba(255, 255, 255, 10);
    width: 8px;
    border-radius: 4px;
    padding: 2px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 40);
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 60);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: transparent;
    height: 0;
    border: none;
}

QScrollBar:horizontal {
    background: rgba(255, 255, 255, 10);
    height: 8px;
    border-radius: 4px;
    padding: 2px;
}

QScrollBar::handle:horizontal {
    background: rgba(255, 255, 255, 40);
    border-radius: 4px;
    min-width: 30px;
}

/* Glass Switch Button */
SwitchButton {
    background-color: rgba(0, 0, 0, 100);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 10px;
}

SwitchButton::groove:horizontal {
    background: rgba(255, 255, 255, 20);
    border-radius: 8px;
    height: 16px;
}

SwitchButton::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ffffff, stop:1 #e0e0e0);
    border-radius: 8px;
    width: 20px;
    margin: -2px 0;
}

/* Glass Progress Bar */
QProgressBar {
    background-color: rgba(0, 0, 0, 100);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 8px;
    text-align: center;
    color: #ffffff;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6495ED, stop:1 #87CEEB);
    border-radius: 6px;
}

/* Glass Separators */
HorizontalSeparator {
    background: rgba(255, 255, 255, 20);
    border: none;
    height: 1px;
    border-radius: 1px;
}

/* Glass Tool Button */
TransparentToolButton {
    background-color: rgba(255, 255, 255, 10);
    border: 1px solid rgba(255, 255, 255, 20);
    border-radius: 8px;
}

TransparentToolButton:hover {
    background-color: rgba(255, 255, 255, 25);
    border: 1px solid rgba(255, 255, 255, 50);
}

/* Glass Labels */
TitleLabel, SubtitleLabel, StrongBodyLabel {
    color: #ffffff;
    background: transparent;
}

QLabel {
    color: rgba(255, 255, 255, 220);
    background: transparent;
}

/* Stack Widget Container */
QStackedWidget {
    background: transparent;
    border: none;
}

/* Group Box */
QGroupBox {
    background-color: rgba(30, 30, 40, 180);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
    font-weight: 500;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    color: #ffffff;
}

/* Tooltip */
QToolTip {
    background-color: rgba(40, 40, 50, 230);
    border: 1px solid rgba(255, 255, 255, 30);
    border-radius: 8px;
    padding: 8px 12px;
    color: #ffffff;
}

/* Stacked Widget Page */
QWidget[page="true"] {
    background: rgba(0, 0, 0, 30);
    border-radius: 16px;
}
"""

GLASS_LIGHT_STYLESHEET = """
/* Frosted Glass Light Theme */

QMainWindow {
    background: transparent;
}

QWidget {
    color: #1a1a2e;
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

/* Glass Window Background */
FluentWindow > QWidget#qt_central_widget {
    background: transparent;
}

/* Glass Cards - Semi-transparent with blur effect simulation */
SimpleCardWidget, CardWidget {
    background-color: rgba(255, 255, 255, 180);
    border: 1px solid rgba(0, 0, 0, 20);
    border-radius: 16px;
    padding: 16px;
}

/* Glass Card Hover Effect */
SimpleCardWidget:hover, CardWidget:hover {
    background-color: rgba(255, 255, 255, 220);
    border: 1px solid rgba(0, 0, 0, 30);
}

/* Navigation Pane - Glass Effect */
QFrame#navigationWidget {
    background-color: rgba(245, 245, 250, 150);
    border: none;
    border-right: 1px solid rgba(0, 0, 0, 15);
}

/* Navigation Items */
QPushButton[navButton="true"] {
    background-color: rgba(255, 255, 255, 80);
    border: 1px solid rgba(0, 0, 0, 15);
    border-radius: 8px;
    padding: 8px 12px;
    text-align: left;
    color: #1a1a2e;
}

QPushButton[navButton="true"]:hover {
    background-color: rgba(255, 255, 255, 150);
    border: 1px solid rgba(0, 0, 0, 25);
}

QPushButton[navButton="true"]:checked {
    background-color: rgba(100, 149, 237, 150);
    border: 1px solid rgba(100, 149, 237, 150);
    color: #ffffff;
}

/* Glass Buttons */
PrimaryPushButton, PushButton {
    background-color: rgba(100, 149, 237, 200);
    border: 1px solid rgba(100, 149, 237, 150);
    border-radius: 8px;
    padding: 8px 20px;
    color: #ffffff;
    font-weight: 500;
}

PrimaryPushButton:hover, PushButton:hover {
    background-color: rgba(120, 169, 255, 220);
    border: 1px solid rgba(120, 169, 255, 200);
}

PrimaryPushButton:pressed, PushButton:pressed {
    background-color: rgba(80, 129, 207, 200);
}

PushButton {
    background-color: rgba(255, 255, 255, 180);
    border: 1px solid rgba(0, 0, 0, 30);
    color: #1a1a2e;
}

PushButton:hover {
    background-color: rgba(255, 255, 255, 220);
}

/* Glass Input Fields */
LineEdit, ComboBox {
    background-color: rgba(255, 255, 255, 150);
    border: 1px solid rgba(0, 0, 0, 30);
    border-radius: 8px;
    padding: 10px 12px;
    color: #1a1a2e;
    selection-background-color: rgba(100, 149, 237, 150);
}

LineEdit:focus, ComboBox:focus {
    border: 1px solid rgba(100, 149, 237, 180);
    background-color: rgba(255, 255, 255, 200);
}

LineEdit::placeholder, ComboBox::placeholder {
    color: rgba(0, 0, 0, 100);
}

/* ComboBox Dropdown */
QComboBox QAbstractItemView {
    background-color: rgba(255, 255, 255, 230);
    border: 1px solid rgba(0, 0, 0, 30);
    border-radius: 8px;
    selection-background-color: rgba(100, 149, 237, 150);
    color: #1a1a2e;
}

/* Glass List Widget */
ListWidget {
    background-color: rgba(255, 255, 255, 100);
    border: 1px solid rgba(0, 0, 0, 20);
    border-radius: 12px;
    padding: 8px;
    color: #1a1a2e;
}

ListWidget::item {
    background-color: rgba(255, 255, 255, 150);
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 10px 12px;
    margin: 2px 0;
}

ListWidget::item:selected {
    background-color: rgba(100, 149, 237, 150);
    border: 1px solid rgba(100, 149, 237, 150);
    color: #ffffff;
}

ListWidget::item:hover {
    background-color: rgba(100, 149, 237, 50);
}

/* Glass Scroll Area */
ScrollArea {
    background: transparent;
    border: none;
}

ScrollArea > QWidget > QWidget {
    background: transparent;
}

/* Glass Scrollbars */
QScrollBar:vertical {
    background: rgba(0, 0, 0, 10);
    width: 8px;
    border-radius: 4px;
    padding: 2px;
}

QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 40);
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(0, 0, 0, 60);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: transparent;
    height: 0;
    border: none;
}

QScrollBar:horizontal {
    background: rgba(0, 0, 0, 10);
    height: 8px;
    border-radius: 4px;
    padding: 2px;
}

QScrollBar::handle:horizontal {
    background: rgba(0, 0, 0, 40);
    border-radius: 4px;
    min-width: 30px;
}

/* Glass Switch Button */
SwitchButton {
    background-color: rgba(255, 255, 255, 150);
    border: 1px solid rgba(0, 0, 0, 30);
    border-radius: 10px;
}

SwitchButton::groove:horizontal {
    background: rgba(0, 0, 0, 20);
    border-radius: 8px;
    height: 16px;
}

SwitchButton::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #ffffff, stop:1 #f0f0f0);
    border-radius: 8px;
    width: 20px;
    margin: -2px 0;
}

/* Glass Progress Bar */
QProgressBar {
    background-color: rgba(255, 255, 255, 150);
    border: 1px solid rgba(0, 0, 0, 30);
    border-radius: 8px;
    text-align: center;
    color: #1a1a2e;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6495ED, stop:1 #87CEEB);
    border-radius: 6px;
}

/* Glass Separators */
HorizontalSeparator {
    background: rgba(0, 0, 0, 20);
    border: none;
    height: 1px;
    border-radius: 1px;
}

/* Glass Tool Button */
TransparentToolButton {
    background-color: rgba(255, 255, 255, 80);
    border: 1px solid rgba(0, 0, 0, 20);
    border-radius: 8px;
}

TransparentToolButton:hover {
    background-color: rgba(255, 255, 255, 120);
    border: 1px solid rgba(0, 0, 0, 40);
}

/* Glass Labels */
TitleLabel, SubtitleLabel, StrongBodyLabel {
    color: #1a1a2e;
    background: transparent;
}

QLabel {
    color: rgba(0, 0, 0, 180);
    background: transparent;
}

/* Stack Widget Container */
QStackedWidget {
    background: transparent;
    border: none;
}

/* Group Box */
QGroupBox {
    background-color: rgba(255, 255, 255, 180);
    border: 1px solid rgba(0, 0, 0, 20);
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
    font-weight: 500;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    color: #1a1a2e;
}

/* Tooltip */
QToolTip {
    background-color: rgba(255, 255, 255, 230);
    border: 1px solid rgba(0, 0, 0, 30);
    border-radius: 8px;
    padding: 8px 12px;
    color: #1a1a2e;
}

/* Stacked Widget Page */
QWidget[page="true"] {
    background: rgba(255, 255, 255, 30);
    border-radius: 16px;
}
"""

BACKGROUND_DARK = """
QMainWindow {
    background-image: url(:/images/background_dark.png);
    background-position: center;
    background-repeat: repeat;
}
"""

BACKGROUND_LIGHT = """
QMainWindow {
    background-image: url(:/images/background_light.png);
    background-position: center;
    background-repeat: repeat;
}
"""


def get_glass_stylesheet(theme: Theme) -> str:
    """Get the appropriate glass stylesheet based on theme."""
    if theme == Theme.DARK:
        return GLASS_DARK_STYLESHEET
    return GLASS_LIGHT_STYLESHEET


def get_background_stylesheet(theme: Theme) -> str:
    """Get the appropriate background stylesheet based on theme."""
    if theme == Theme.DARK:
        return BACKGROUND_DARK
    return BACKGROUND_LIGHT


def apply_glass_effect(widget, theme: Theme = Theme.DARK, opacity: float = 0.8):
    """Apply glass effect to a widget."""
    stylesheet = get_glass_stylesheet(theme)
    widget.setStyleSheet(stylesheet)


def create_glass_card(parent=None, theme: Theme = Theme.DARK):
    """Create a glass-styled card widget."""
    from qfluentwidgets.components.widgets.card_widget import SimpleCardWidget
    card = SimpleCardWidget(parent)
    card.setStyleSheet(get_glass_stylesheet(theme))
    return card


def create_glass_button(text: str, parent=None, primary: bool = False, theme: Theme = Theme.DARK):
    """Create a glass-styled button."""
    from qfluentwidgets import PrimaryPushButton, PushButton
    if primary:
        button = PrimaryPushButton(text, parent)
    else:
        button = PushButton(text, parent)
    button.setStyleSheet(get_glass_stylesheet(theme))
    return button
