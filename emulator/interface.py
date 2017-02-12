from PyQt5.QtWidgets import (QWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy,
                             QStackedLayout, QSlider)
from PyQt5.QtCore import QSize, Qt, QBasicTimer, QPoint
from PyQt5.QtGui import QIcon, QFont, QImage, qRgb, QPixmap, QTransform
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QScrollArea, QGraphicsView
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor, QPalette


# from emulator.robot import Robot
def get_screen_size():
    rect = QDesktopWidget().screenGeometry()
    return rect.width(), rect.height()


class ControlWidget(QFrame):

    def __init__(self, robot):
        super().__init__()
        self._robot = robot
        self._is_binded_engines = True
        self._is_binded_powers = True
        self._engines_binded_widget = EnginesBindedWidget()
        self._engines_not_binded_widget = EnginesNotBindedWidget()
        self._engines_widget_index = {0: self._engines_not_binded_widget, 1: self._engines_binded_widget}
        self._engines_layout = QStackedLayout()
        self._vbox_main = QVBoxLayout()

        self._bttn_bind_engines = QPushButton("Bind")
        self._bttn_bind_powers = QPushButton("Bind")

        self._l_power = QSlider(Qt.Horizontal)
        self._r_power = QSlider(Qt.Horizontal)

        self._initUI()

    def _initUI(self):
        # ====== Draw ======
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
        lp_txt = QLabel("0")  # presents current power num.
        rp_txt = QLabel("0")  # presents current power num.
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

        lp_txt.setAlignment(Qt.AlignCenter)
        rp_txt.setAlignment(Qt.AlignCenter)
        s_txt_layout = QHBoxLayout()
        s_txt_layout.addSpacing(1)
        s_txt_layout.addWidget(lp_txt)
        s_txt_layout.addSpacing(4)
        s_txt_layout.addWidget(rp_txt)
        s_txt_layout.addSpacing(1)

        bttn_reset = QPushButton("Reset to 0")

        for i in self._engines_widget_index:
            self._engines_layout.addWidget(self._engines_widget_index[i])

        self._vbox_main.addLayout(self._engines_layout)
        self._vbox_main.addWidget(self._bttn_bind_engines)
        self._vbox_main.addStretch(2)
        self._vbox_main.addWidget(ep_lbl)
        self._vbox_main.addLayout(s_lbl_layout)
        self._vbox_main.addLayout(sliders_layout)
        self._vbox_main.addLayout(s_txt_layout)
        self._vbox_main.addWidget(self._bttn_bind_powers)

        self._vbox_main.addWidget(bttn_reset)

        self.setLayout(self._vbox_main)
        self.setGeometry(50, 50, 600, 600)
        self.setWindowTitle('Robot Controller')

        # ====== Bind ======
        self._engines_binded_widget.bttn_forward.clicked.connect(self._robot.both_engines_forward)
        self._engines_binded_widget.bttn_backward.clicked.connect(self._robot.both_engines_backward)
        self._engines_not_binded_widget.bttn_left_forward.clicked.connect(self._robot.left_engine_forward)
        self._engines_not_binded_widget.bttn_left_backward.clicked.connect(self._robot.left_engine_backward)
        self._engines_not_binded_widget.bttn_right_forward.clicked.connect(self._robot.right_engine_forward)
        self._engines_not_binded_widget.bttn_right_backward.clicked.connect(self._robot.right_engine_backward)

        self._bttn_bind_engines.clicked.connect(self._bttn_bind_engines_clicked)
        self._bttn_bind_powers.clicked.connect(self._bttn_bind_powers_clicked)

        self._l_power.valueChanged.connect(lp_txt.setNum)
        self._r_power.valueChanged.connect(rp_txt.setNum)

        self._l_power.valueChanged.connect(self._robot.change_left_engine_power)
        self._r_power.valueChanged.connect(self._robot.change_right_engine_power)

        bttn_reset.clicked.connect(self._power_reset_to_zero)
        self._bind_engines()  # as a default, engines are binded
        self._bind_powers()  # as a default, powers are binded

    def _bind_engines(self):
        self._engines_layout.setCurrentIndex(1)
        self._bttn_bind_engines.setChecked(True)
        self._bttn_bind_engines.setText("Unbind")

    def _bind_powers(self):
        self._l_power.valueChanged.connect(self._r_power.setValue)
        self._r_power.valueChanged.connect(self._l_power.setValue)
        self._bttn_bind_powers.setChecked(True)
        self._bttn_bind_powers.setText("Unbind")

    def _bttn_bind_engines_clicked(self):
        # the button changes its "isChecked" just after being clicked, so isChecked shows actual state
        if self._bttn_bind_engines.isChecked():
            self._engines_layout.setCurrentIndex(1)
            self._bttn_bind_engines.setText("Unbind")
        else:
            self._engines_layout.setCurrentIndex(0)
            self._bttn_bind_engines.setText("Bind")

    def _bttn_bind_powers_clicked(self):
        if self._bttn_bind_powers.isChecked():
            self._l_power.valueChanged.connect(self._r_power.setValue)
            self._r_power.valueChanged.connect(self._l_power.setValue)
            self._bttn_bind_powers.setText("Unbind")
        else:
            self._l_power.valueChanged.disconnect(self._r_power.setValue)
            self._r_power.valueChanged.disconnect(self._l_power.setValue)
            self._bttn_bind_powers.setText("Bind")

    def _power_reset_to_zero(self):
        self._l_power.setValue(0)
        self._r_power.setValue(0)


class EnginesBindedWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.bttn_forward = QPushButton()
        self.bttn_backward = QPushButton()
        self._initUI()

    def _initUI(self):
        vbox_engine = QVBoxLayout()
        self.bttn_forward.setIcon(QIcon("./assets/arrow-up.png"))
        self.bttn_backward.setIcon(QIcon("./assets/arrow-down.png"))
        vbox_engine.addWidget(self.bttn_forward)
        vbox_engine.addWidget(self.bttn_backward)
        vbox_engine.addStretch(1)

        self.setLayout(vbox_engine)


class EnginesNotBindedWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.bttn_left_forward = QPushButton()
        self.bttn_left_backward = QPushButton()
        self.bttn_right_forward = QPushButton()
        self.bttn_right_backward = QPushButton()
        self._initUI()

    def _initUI(self):
        hbox_engine = QHBoxLayout()
        vbox_left = QVBoxLayout()
        vbox_right = QVBoxLayout()

        self.bttn_left_forward.setIcon(QIcon("./assets/arrow-up.png"))
        self.bttn_left_backward.setIcon(QIcon("./assets/arrow-down.png"))
        self.bttn_right_forward.setIcon(QIcon("./assets/arrow-up.png"))
        self.bttn_right_backward.setIcon(QIcon("./assets/arrow-down.png"))
        lbl_l = QLabel("L")
        lbl_r = QLabel("R")
        lbl_l.setAlignment(Qt.AlignCenter)
        lbl_r.setAlignment(Qt.AlignCenter)
        lbl_r.setFixedHeight(30)
        lbl_l.setFixedHeight(30)

        vbox_left.addWidget(lbl_l)
        vbox_left.addWidget(self.bttn_left_forward)
        vbox_left.addWidget(self.bttn_left_backward)
        vbox_left.addStretch(1)

        vbox_right.addWidget(lbl_r)
        vbox_right.addWidget(self.bttn_right_forward)
        vbox_right.addWidget(self.bttn_right_backward)
        vbox_right.addStretch(1)

        hbox_engine.addLayout(vbox_left)
        hbox_engine.addLayout(vbox_right)

        self.setLayout(hbox_engine)


# Draws the robot and the maze on the canvas. Checks collisions
class BoardWidget(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.timer = QBasicTimer()
        self._width = width
        self._height = height
        self._robot_pixmap = QPixmap("./assets/robo.png")
        self._robot_depicted_width = self._robot_pixmap.width()
        self._robot_depicted_height = self._robot_pixmap.height()
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
        self.draw_robot(0, 0, 0, (0, 0))

    def draw_robot(self, left_top_pos, angle, rotation_point):
        painter = QPainter(self._board_pixmap)
        xc, yc = rotation_point  # point to rotate around
        painter.translate(xc, yc)
        painter.rotate(angle)
        x, y = left_top_pos
        target = QRect(x + 1, y + 1, self._robot_depicted_width, self._robot_depicted_height)
        source = QRect(0., 0., self._robot_pixmap.width(), self._robot_pixmap.height())
        painter.drawPixmap(target, self._robot_pixmap, source)
        self._label.setPixmap(self._board_pixmap)
        painter.end()

    def get_size(self):
        return self._width, self._height


# Joins control widget and the board
class MainView(QWidget):

    def __init__(self):
        super().__init__()
        self._board_view = BoardWidget()
        # self._robot = Robot(self._board_view.draw_robot, 0, 0, 180)  # rotation vector is reverted
        self._control = ControlWidget(self._robot)
        self.initUI()
        self.show()
        self._hscale_factor = 1
        self._vscale_factor = 1

    def initUI(self):
        layout = QBoxLayout(QBoxLayout.RightToLeft, self)
        layout.addWidget(self._control)
        layout.addStretch(1)
        layout.addWidget(self._board_view)
        self.setLayout(layout)
        self.setWindowTitle('Robot Emulator')
        self.setWindowIcon(QIcon("./assets/robo.png"))
        self._board_view.update()

    def draw_board(self, board):
        # update scale factors
        pass

    def draw_robot(self, left_top_pos, angle):
        pass