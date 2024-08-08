import os

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import *
from config import *

class ItemWidget(QWidget):
    def __init__(self, title: str):
        super(ItemWidget, self).__init__()

        self.layout = QHBoxLayout(self)
        t = QLabel(title)
        t.setMinimumWidth(100)
        self.layout.addWidget(t)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

class DirSelectorWidget(ItemWidget):
    def __init__(self, title: str, key: str):
        super().__init__(title)
        widget = QWidget()
        layout = QHBoxLayout(widget)

        self.lineedit = QLineEdit()
        self.lineedit.setReadOnly(True)
        self.lineedit.textChanged.connect(self.save_)

        layout.addWidget(self.lineedit)

        btn = QPushButton("选择")
        layout.addWidget(btn)
        btn.clicked.connect(self.showDialog)
        self.addWidget(widget)

        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.lineedit.setText(data[self.key])

    def save_(self):
        update_config(self.key, self.lineedit.text())

    def showDialog(self):
        dir_name = QFileDialog.getExistingDirectory(self, '选择目录', os.path.dirname(self.lineedit.text()))
        if dir_name:
            self.lineedit.setText(dir_name)

class LineEditWidget(ItemWidget):
    def __init__(self, title: str, key: str):
        super().__init__(title)
        widget = QWidget()
        layout = QHBoxLayout(widget)

        self.lineedit = QLineEdit()
        self.lineedit.setEchoMode(QLineEdit.Password)
        self.lineedit.textChanged.connect(self.save_)

        layout.addWidget(self.lineedit)

        self.addWidget(widget)

        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.lineedit.setText(data[self.key])

    def save_(self):
        update_config(self.key, self.lineedit.text())
