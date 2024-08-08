from PySide6 import QtCore, QtGui, QtWidgets
from main_window import Window
import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = Window()
    ui.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
