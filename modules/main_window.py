from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
)


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Configurações da Janela Principal
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()  # Create a vertical layout
        self.cw.setLayout(self.vLayout)  # Set the layout for the central widget
        self.setCentralWidget(self.cw)

        # titulo da janela
        self.setWindowTitle("Calculadora")  # Set the window title

    def AjustFixedSize(self):
        # Ultima Coisa a ser feita
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())  # Set the window to a fixed size

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)  # Add a widget to the vertical layout

    def makeMsgBox(self):
        return QMessageBox(self)
