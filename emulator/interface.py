from PyQt5.QtWidgets import (QPushButton, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                             QComboBox, QRadioButton, QFileDialog, QLineEdit, QTextEdit)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont


class mainWidget(QWidget):
    def __init__(self):
        super(mainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.show()