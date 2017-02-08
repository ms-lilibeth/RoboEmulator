from PyQt5.QtWidgets import (QWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy,
                             QStackedLayout, QSlider, QLineEdit, QTextEdit)
from PyQt5.QtCore import QSize, Qt, QBasicTimer, QPoint
from PyQt5.QtGui import QIcon, QFont, QImage, qRgb, QPixmap, QTransform
import os
import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QScrollArea, QGraphicsView
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QColor, QPalette


def get_screen_size():
    rect = QDesktopWidget().screenGeometry()
    return rect.width(), rect.height()


# Joins control widget and the board
class Emulator(QWidget):
    def __init__(self):
        super().__init__()
        self._control = ControlWidget()
        self._board = BoardWidget()
        self.initUI()
        self.show()

    def initUI(self):
        layout = QBoxLayout(QBoxLayout.RightToLeft, self)
        layout.addWidget(self._control)
        layout.addStretch(1)
        layout.addWidget(self._board)
        self.setLayout(layout)
        self.setWindowTitle('Robot Emulator')
        self.setWindowIcon(QIcon("./assets/robo.png"))
        self._board.update()


class ControlWidget(QFrame):
    def __init__(self):
        super().__init__()
        self._is_binded_engines = True
        self._is_binded_powers = True
        self._engines_binded_widget = EnginesBindedWidget()
        self._engines_not_binded_widget = EnginesNotBindedWidget()
        self._engines_layout = QStackedLayout()
        self._vbox_main = QVBoxLayout()

        self._bttn_bind_engines = QPushButton("Bind")
        self._bttn_bind_powers = QPushButton("Bind")

        self._l_power = QSlider(Qt.Horizontal)
        self._r_power = QSlider(Qt.Horizontal)
        self._lp_txt = QLabel("0")  # presents current power num.
        self._rp_txt = QLabel("0")  # presents current power num.

        self._initUI()

    def _initUI(self):
        self._bttn_bind_engines.setCheckable(True)
        self._bttn_bind_powers.setCheckable(True)

        self._l_power.setMinimum(-100)
        self._l_power.setMaximum(100)
        self._r_power.setMinimum(-100)
        self._r_power.setMaximum(100)
        self._l_power.setTickInterval(1)
        self._r_power.setTickInterval(1)

        ep_lbl = QLabel("Engine Power")
        ep_lbl.setAlignment(Qt.AlignCenter)

        lp_label = QLabel("L")
        rp_label = QLabel("R")
        s_lbl_layout = QHBoxLayout()  # contains L and R labels for sliders
        s_lbl_layout.addStretch(1)
        s_lbl_layout.addWidget(lp_label)
        s_lbl_layout.addStretch(2)
        s_lbl_layout.addWidget(rp_label)
        s_lbl_layout.addStretch(1)

        sliders_layout = QHBoxLayout()
        sliders_layout.addWidget(self._l_power)
        sliders_layout.addSpacing(1)
        sliders_layout.addWidget(self._r_power)

        self._lp_txt.setAlignment(Qt.AlignCenter)
        self._rp_txt.setAlignment(Qt.AlignCenter)
        # self._lp_txt.setFixedSize(50, 30)
        s_txt_layout = QHBoxLayout()
        s_txt_layout.addSpacing(1)
        s_txt_layout.addWidget(self._lp_txt)
        s_txt_layout.addSpacing(4)
        s_txt_layout.addWidget(self._rp_txt)
        s_txt_layout.addSpacing(1)

        self._engines_layout.addWidget(self._engines_binded_widget)
        self._engines_layout.addWidget(self._engines_not_binded_widget)
        self._vbox_main.addLayout(self._engines_layout)
        self._vbox_main.addWidget(self._bttn_bind_engines)
        self._vbox_main.addStretch(1)
        self._vbox_main.addWidget(ep_lbl)
        self._vbox_main.addLayout(s_lbl_layout)
        self._vbox_main.addLayout(sliders_layout)
        self._vbox_main.addLayout(s_txt_layout)
        self._vbox_main.addWidget(self._bttn_bind_powers)

        self.setLayout(self._vbox_main)
        self.setGeometry(50, 50, 600, 600)
        self.setWindowTitle('Robot Controller')


class EnginesBindedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        vbox_engine = QVBoxLayout()
        bttn_forward, bttn_backward = QPushButton(), QPushButton()
        bttn_forward.setIcon(QIcon("./assets/arrow-up.png"))
        bttn_backward.setIcon(QIcon("./assets/arrow-down.png"))
        vbox_engine.addWidget(bttn_forward)
        vbox_engine.addWidget(bttn_backward)
        vbox_engine.addStretch(1)

        self.setLayout(vbox_engine)


class EnginesNotBindedWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        hbox_engine = QHBoxLayout()
        vbox_left = QVBoxLayout()
        vbox_right = QVBoxLayout()
        bttn_left_forward = QPushButton()
        bttn_left_backward = QPushButton()
        bttn_right_forward = QPushButton()
        bttn_right_backward = QPushButton()
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
        vbox_left.addStretch(1)

        vbox_right.addWidget(lbl_r)
        vbox_right.addWidget(bttn_right_forward)
        vbox_right.addWidget(bttn_right_backward)
        vbox_right.addStretch(1)

        hbox_engine.addLayout(vbox_left)
        hbox_engine.addLayout(vbox_right)

        self.setLayout(hbox_engine)

# Draws the robot and the maze on the canvas. Checks collisions
class BoardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QBasicTimer()
        self._width = 300
        self._height = 300
        self._robot_pixmap = QPixmap("./assets/robo.png")
        self._board_pixmap = QPixmap(self._width, self._height)
        self._board_pixmap.fill(QColor(0xffffff))
        self._label = QLabel()
        self._label.setPixmap(self._board_pixmap)
        self._layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        scroll = QScrollArea()
        scroll.setBackgroundRole(QPalette.Dark)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(self._label)
        scroll.setWidgetResizable(True)

        self._layout.addWidget(scroll)
        self.setLayout(self._layout)
        self.setMinimumSize(300, 300)
        self.setWindowTitle("Robot Emulator")

    def wheelEvent(self, event):
        pass

    def paintEvent(self, QPaintEvent):
        self.draw_robot(0, 0, 0)

    def draw_robot(self, x, y, angle):
        painter = QPainter(self._board_pixmap)
        xc, yc = 75, 75  # point to rotate around
        painter.translate(xc, yc)
        painter.rotate(angle)
        target = QRectF(x + 1, y + 1, 60, 40)
        source = QRectF(0., 0., self._robot_pixmap.width(), self._robot_pixmap.height())
        # painter.fillRect(x + 1, y + 1, 60, 40, QColor(0x000000))
        painter.drawPixmap(target, self._robot_pixmap, source)
        self._label.setPixmap(self._board_pixmap)
        painter.end()
