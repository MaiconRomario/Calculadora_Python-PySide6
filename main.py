import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from modules.info import Info
from modules.main_window import MainWindow
from utils.variables import WINDOW_ICON_PATH
from modules.display import Display
from modules.buttons import ButtonsGrid
from utils.styles import setupTheme


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)

    setupTheme(app)
    window = MainWindow()

    # info
    info = Info("Sua conta")
    window.addWidgetToVLayout(info)

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)  # Set the window icon
    app.setWindowIcon(icon)  # Set the application icon

    # Display
    display = Display("")
    window.addWidgetToVLayout(display)

    # grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # Executa tudo
    window.AjustFixedSize()
    window.show()
    app.exec()
