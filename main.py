import sys

from PyQt6 import QtGui, QtWidgets

from app.app_config import load_app_settings
from app.main_window import MainWindow


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QtGui.QFont('Microsoft YaHei', 10))
    settings = load_app_settings()
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
