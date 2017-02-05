from PyQt5.QtWidgets import (QDesktopWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import QSize, Qt, QBasicTimer, QPoint
from PyQt5.QtGui import QIcon, QFont, QImage, qRgb, QPixmap, QTransform
import os
import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QColor


def get_screen_size():
    rect = QDesktopWidget().screenGeometry()
    return rect.width(), rect.height()


class Emulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tboard = Board(self)
        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.tboard)
        self.resize(300, 300)
        self.center()
        self.setWindowTitle('Emulator')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


# Draws the robot and the maze on the canvas. Checks collisions
class Board(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        # if not os.path.exists(img_filepath):
        #     raise ValueError("Image does not exist")
        self.timer = QBasicTimer()
        # self.img = QImage().load(img_filepath)
        self._layout_main = QHBoxLayout()
        # self._field = QPixmap(300, 300)
        self._robot_pixmap = QPixmap("robo.png")
        self.initUI()
        self.show()

    def initUI(self):
        # self._field.fill(Qt.white)
        # lbl = QLabel(self)
        # lbl.setPixmap(self._field)
        # lbl.setFixedSize(300, 300)
        # self._layout_main.addWidget(lbl)
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('roboCanvas')
        # scroll = QtGui.QScrollArea()
        # scroll.setWidget(mygroupbox)
        # scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        # layout.addWidget(scroll)

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        self.draw_robot(painter, 50, 50)

    def draw_robot(self, painter, x, y):
        color = QColor(0x000000)
        xc, yc = 75, 75
        painter.translate(xc, yc)
        painter.rotate(45)
        target = QRectF(x + 1, y + 1, 60, 40)
        source = QRectF(0., 0., self._robot_pixmap.width(), self._robot_pixmap.height())
        painter.drawPixmap(target, self._robot_pixmap, source)
        # painter.fillRect(x + 1, y + 1, 60, 40, color)
        painter.resetTransform()
