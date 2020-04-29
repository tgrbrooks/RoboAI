# Local imports
from display.controlpanel import ControlPanel

# Standard imports
import sys

# pyqt5 imports
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = ControlPanel()
    
    sys.exit(app.exec_())
