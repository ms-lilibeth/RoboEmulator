from PyQt5.QtWidgets import (QWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy)
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


# Joins control widget and the board
class Emulator(QWidget):
    def __init__(self):
        super().__init__()
        self._control = ControlWidget()
        self._board = BoardWidget()
        # self._board.show()
        # self._control.show()
        self.initUI()
        self.show()

    def initUI(self):
        layout = QBoxLayout(QBoxLayout.RightToLeft, self)
        layout.addWidget(self._control)
        layout.addStretch(1)
        layout.addWidget(self._board)
        self.setLayout(layout)
        # self.center()
        self.setWindowTitle('Robot Emulator')
        self.setWindowIcon(QIcon("./assets/robo.png"))
        self._board.update()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class ControlWidget(QFrame):
    def __init__(self):
        super().__init__()
        self._engines_binded = True
        self._powers_binded = True
        self._engines_layout = None
        self._vbox_main = QVBoxLayout()
        self.initUI()
        # self.show()

    def initUI(self):
        if self._engines_binded:
            self._engines_layout = self._get_engines_binded_layout()
        else:
            self._engines_layout = self._get_engines_not_binded_layout()
        self._vbox_main.addLayout(self._engines_layout)
        self.setLayout(self._vbox_main)
        self.setGeometry(50, 50, 600, 600)
        self.setWindowTitle('Robot Controller')

    def _get_engines_binded_layout(self):
        vbox_engine = QVBoxLayout()
        bttn_forward, bttn_backward = QPushButton(), QPushButton()
        bttn_forward.setIcon(QIcon("./assets/arrow-up.png"))
        bttn_backward.setIcon(QIcon("./assets/arrow-down.png"))
        vbox_engine.addWidget(bttn_forward)
        vbox_engine.addWidget(bttn_backward)
        return vbox_engine

    def _get_engines_not_binded_layout(self):
        hbox_engine = QHBoxLayout()
        vbox_left = QVBoxLayout()
        vbox_right = QVBoxLayout()

        bttn_left_forward, bttn_left_backward, bttn_right_forward, bttn_right_backward = QPushButton(), QPushButton(), \
                                                                                         QPushButton(), QPushButton()

        bttn_left_forward.setIcon(QIcon("./assets/arrow-up.png"))
        bttn_left_backward.setIcon(QIcon("./assets/arrow-down.png"))
        bttn_right_forward.setIcon(QIcon("./assets/arrow-up.png"))
        bttn_right_backward.setIcon(QIcon("./assets/arrow-down.png"))
        lbl_l = QLabel("L")
        lbl_r = QLabel("R")
        lbl_l.setAlignment(Qt.AlignCenter)
        lbl_r.setAlignment(Qt.AlignCenter)
        lbl_r.setFixedHeight(30)
        lbl_l.setFixedHeight(30)

        vbox_left.addWidget(lbl_l)
        vbox_left.addWidget(bttn_left_forward)
        vbox_left.addWidget(bttn_left_backward)

        vbox_right.addWidget(lbl_r)
        vbox_right.addWidget(bttn_right_forward)
        vbox_right.addWidget(bttn_right_backward)

        hbox_engine.addLayout(vbox_left)
        hbox_engine.addLayout(vbox_right)
        return hbox_engine


# Draws the robot and the maze on the canvas. Checks collisions
class BoardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QBasicTimer()
        self._width = 300
        self._height = 300
        self._robot_pixmap = QPixmap("robo.png")
        # self._board = [0 for i in range(self._width*self._height)]
        self.initUI()
        # self.show()
        # self.update()

    def initUI(self):
        self.setStyleSheet("QWidget { background: #123456 }")
        self.setFixedSize(300, 300)
        self.setWindowTitle("Robot Emulator")
        # self._field.fill(Qt.red)
        # lbl = QLabel()
        # lbl.setPixmap(self._field)
        # lbl.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # lbl.setFixedSize(300, 300)
        # self._layout_main.addWidget(lbl)
        # self.setGeometry(300, 300, 280, 170)
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
