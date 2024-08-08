from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import *
import os
from setting_item import DirSelectorWidget, LineEditWidget
from core import *

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()
        self.worker = GenerateThread()
        self.worker.finished.connect(self.finish)

    def initUI(self):
        self.setWindowTitle('U++ Document Generate')

        layout = QVBoxLayout(self)

        layout.addWidget(DirSelectorWidget("搜索目录", "search_path"))
        layout.addWidget(LineEditWidget("API KEY", "api_key"))

        self.start_btn = QPushButton("生成Markdown")
        self.start_btn.setFixedHeight(30)
        self.start_btn.clicked.connect(self.start)


        layout.addWidget(self.start_btn)

        self.text_browser = QTextBrowser()

        layout.addWidget(self.text_browser)

        copy_btn = QPushButton("复制到剪贴板")
        copy_btn.clicked.connect(self.copy_markdown)
        copy_btn.setFixedHeight(30)
        layout.addWidget(copy_btn)


        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.resize(600, 800)



    def start(self):
        self.text_browser.clear()
        self.worker.start()
        self.start_btn.setEnabled(False)

    def finish(self, markdown_text):
        self.start_btn.setEnabled(True)
        self.text_browser.setText(markdown_text)

    def copy_markdown(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_browser.toPlainText())
