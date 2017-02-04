from PyQt5.QtWidgets import (QDesktopWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import QSize, Qt, QBasicTimer, QPoint
from PyQt5.QtGui import QIcon, QFont, QImage, QPainter, qRgb, QPixmap, QTransform
import os


def get_screen_size():
    rect = QDesktopWidget().screenGeometry()
    return rect.width(), rect.height()


# Draws the robot and the maze on the canvas. Checks collisions
class Board(QWidget):
    def __init__(self, img_filepath):
        if not os.path.exists(img_filepath):
            raise ValueError("Image does not exist")
        super(Board, self).__init__()
        self.timer = QBasicTimer()
        self.img = QImage().load(img_filepath)
        self._layout_main = QHBoxLayout()
        self._field = QPixmap(300, 300)
        self.initUI()

    def initUI(self):
        self._field.fill(Qt.white)
        lbl = QLabel(self)
        lbl.setPixmap(self._field)
        lbl.setFixedSize(300, 300)
        self._layout_main.addWidget(lbl)
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('roboCanvas')
        # scroll = QtGui.QScrollArea()
        # scroll.setWidget(mygroupbox)
        # scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)        #
        # layout.addWidget(scroll)
        pass

    def _rotate_robo(self, angle):
        # t = QTransform()
        # # Do not forget to substract the rect size to center it on self._center
        # t.translate(self._center.x() - rect.width() / 2, self._center.y() - rect.height() / 2)
        #
        # t.translate(rect.width() / 2, rect.height() / 2)
        # t.rotate(45.0)
        # t.translate(-rect.width() / 2, -rect.height() / 2)
        pass

    def _resize_image(self, image, new_size):
        if image.size() == new_size:
            return

        new_img = QImage(new_size, QImage.Format_RGB32)
        new_img.fill(qRgb(255, 255, 255))
        painter = QPainter(new_img)
        painter.drawImage(QPoint(0, 0), image)
        self.image = new_img

    def draw_robot(self, position, angle):
        pass


class Robot:
    _center_position = None
    _angle = 0

    def __init__(self):
        pass


class ControlWidget(QWidget):
    def __init__(self):
        super(ControlWidget, self).__init__()
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
        self.setWindowTitle('RoboEmulator')
        # self.setWindowIcon(QIcon("./icons/main.png"))

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


# groups RobotCanvas and Control widgets
class MainWidget(QWidget):
    def __init__(self):
        # self.resize(250, 150)
        self.center()
