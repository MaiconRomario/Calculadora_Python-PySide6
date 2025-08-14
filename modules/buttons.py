from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget
from utils.variables import MEDIUM_FONT_SIZE
from utils.utils import isNumOrDot, isEmpty, isValidNumber, converToNumber
from PySide6.QtCore import Slot
import math


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from info import Info
    from main_window import MainWindow


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configStyle()

    def configStyle(self):
        font = self.font()  # Set the font for the button
        font.setPixelSize(MEDIUM_FONT_SIZE)  # Set the font size
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(
        self, display: "Display", info: "Info", window: "MainWindow", *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ["C", "◀", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["N", "0", ".", "="],
        ]
        self.display = display  # Store the display widget
        self.info = info
        self._equation = ""
        self._equationInitialValue = "Sua conta"
        self._left = None
        self._right = None
        self._op = None
        self.window = window

        self.equation = self._equationInitialValue  # Initialize the equation
        self._makeGride()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value: str):
        self._equation = value
        self.info.setText(value)  # Update the info label with the new equation

    def _makeGride(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for i, row in enumerate(self._gridMask):
            for j, ButtonText in enumerate(row):
                button = Button(ButtonText)

                if not isNumOrDot(ButtonText) and not isEmpty(ButtonText):
                    button.setProperty("cssClass", "specialButton")
                    self.configSpecialButtons(button)

                self.addWidget(button, i, j)  # Add the button to the grid layout

                slot = self._makeSlot(
                    self._insertToDisplay,
                    ButtonText,
                )

                self._connectButtonClicked(
                    button, slot
                )  # Connect the button click to the slot

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def configSpecialButtons(self, button):
        text = button.text()
        if text == "C":
            self._connectButtonClicked(button, self._clear)

        if text == "◀":
            self._connectButtonClicked(button, self.display.backspace)

        if text == "N":
            self._connectButtonClicked(button, self._invertNumber)

        if text in "+-/*^":
            self._connectButtonClicked(button, self._makeSlot(self._configLeftOp, text))

        if text == "=":
            self._connectButtonClicked(button, self._eq)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)

        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return

        number = -converToNumber(displayText)

        self.display.setText(str(number))

    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()
        self.display.setFocus()

        # Se a pessoa clicou no operador sem
        # configurar qualquer número
        if not isValidNumber(displayText) and self._left is None:
            self._showError("Você Não digitou nada.")
            return

        # Se houver algo no número da esquerda,
        # não fazemos nada. Aguardaremos o número da direita.
        if self._left is None:
            self._left = converToNumber(displayText)

        self._op = text
        self.equation = (
            f"{self._left} {self._op} ??"  # Update the equation in the info label
        )

    @Slot()
    def _eq(self):
        displayText = self.display.text()
        if not isValidNumber(displayText) or self._left is None:
            self._showError("Conta incompleta.")
            return

        self._right = converToNumber(displayText)
        self.equation = f"{self._left} {self._op} {self._right}"
        result = "error"
        try:
            if "^" in self.equation and isinstance(self._left, int | float):
                result = math.pow(self._left, self._right)
                result = converToNumber(str(result))
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self._showError("Divisão por zero.")
        except OverflowError:
            self._showError("Essa conta não pode ser realizada.")

        self.display.clear()
        self.info.setText(f"{self.equation} = {result}")
        self._left = result
        self._right = None
        self.display.setFocus()

        if result == "error":
            self._left = None

    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()
