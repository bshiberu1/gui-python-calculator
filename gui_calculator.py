#!/usr/bin/env python3

# Filename: pycalc.py

"""PyCalc is a simple calculator built using Python and PyQt5."""
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

from functools import partial

__version__ = '0.1'
__author__ = 'Barry'
ERROR_MSG = 'ERROR'

def evaluateExpression(expression):
    try:
        result = str(eval(expression))
        # result = str(eval(expression, {}, {}))
        print(result)
    except Exception:
        result = ERROR_MSG

    return result

# Create a subclass of QMainWindow to setup the calculator's GUI
class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Calculator')
        self.setFixedSize(400, 400)
        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self._centralWidget.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QLineEdit()
        # Set some display's properties
        self.display.setFixedHeight(60)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonLayout = QGridLayout()
        self.pushButtons = {}

        buttons = {
        "%":(0,0),
        "CE":(0,1),
        "C":(0,2),
        "DEL":(0,3),
        # "1/x":(1,0),
        # "x^2":(1,1),
        # "sqrt":(1,2),
        "/":(1,3),
        "7":(2,0),
        "8":(2,1),
        "9":(2,2),
        "*":(1,2),
        "4":(3,0),
        "5":(3,1),
        "6":(3,2),
        "-":(1,1),
        "1":(4,0),
        "2":(4,1),
        "3":(4,2),
        "+":(1,0),
        "**":(2,3),
        "0":(4,3),
        ".":(3,3),
        "=":(4,3),
        }

        for butText, pos in buttons.items():
            self.pushButtons[butText] = QPushButton(butText)
            self.pushButtons[butText].setFixedSize(80, 45)
            self.buttonLayout.addWidget(self.pushButtons[butText], pos[0], pos[1])
        
        self.generalLayout.addLayout(self.buttonLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText("")

# Create a Controller class to connect the GUI and the model
class PyCalcCtrl:
    """PyCalc Controller class."""
    def __init__(self, view, model):
        """Controller initializer."""
        self._view = view
        self._evaluate = model
        # Connect signals and slots
        self._connectSignals()

    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText())
        # print(result)
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.pushButtons.items():
            if btnText not in {"=", "C"}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.pushButtons["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.pushButtons["C"].clicked.connect(self._view.clearDisplay)

# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    pycalc = QApplication(sys.argv)
    
    # Show the calculator's GUI
    view = PyCalcUi()
    view.show()

    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view)
    # Execute the calculator's main loop
    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()


# import sys

# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QLabel
# from PyQt5.QtWidgets import QWidget

# app = QApplication(sys.argv)

# window = QWidget()
# window.setWindowTitle('PyQt5 App')
# window.setGeometry(100, 100, 280, 80)
# window.move(60, 15)

# helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
# helloMsg.move(60, 15)

# window.show()
# sys.exit(app.exec_())