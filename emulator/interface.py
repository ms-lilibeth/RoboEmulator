from PyQt5.QtWidgets import (QWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy,
                             QStackedLayout, QSlider)
from PyQt5.QtCore import QSize, Qt, QBasicTimer, QPoint
from PyQt5.QtGui import QIcon, QFont, QImage, qRgb, QPixmap, QTransform
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QScrollArea, QGraphicsView
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor, QPalette
import sys, os

robot_image_path = "./assets/robo.png"
if not os.path.exists(robot_image_path):
    print("WARNING: Image ", robot_image_path, " does not exist!")


def get_screen_size():
    rect = QDesktopWidget().screenGeometry()
    return rect.width(), rect.height()


class ControlWidget(QFrame):

    def __init__(self):
        super().__init__()
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

        bttn_reset.clicked.connect(self._power_reset_to_zero)
        self._l_power.valueChanged.connect(lp_txt.setNum)
        self._r_power.valueChanged.connect(rp_txt.setNum)

        self._bttn_bind_engines.clicked.connect(self._bttn_bind_engines_clicked)
        self._bttn_bind_powers.clicked.connect(self._bttn_bind_powers_clicked)

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

    def set_left_forward_handler(self, handler):
        self._engines_not_binded_widget.bttn_left_forward.clicked.connect(handler)

    def set_left_backward_handler(self, handler):
        self._engines_not_binded_widget.bttn_left_backward.clicked.connect(handler)

    def set_right_forward_handler(self, handler):
        self._engines_not_binded_widget.bttn_right_forward.clicked.connect(handler)

    def set_right_backward_handler(self, handler):
        self._engines_not_binded_widget.bttn_right_backward.clicked.connect(handler)

    def set_both_forward_handler(self, handler):
        self._engines_binded_widget.bttn_forward.clicked.connect(handler)

    def set_both_backward_handler(self, handler):
        self._engines_binded_widget.bttn_backward.clicked.connect(handler)

    def set_left_power_changed_handler(self, handler):
        self._l_power.valueChanged.connect(handler)

    def set_right_power_changed_handler(self, handler):
        self._r_power.valueChanged.connect(handler)

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


# Draws the robot and the maze on the canvas
class BoardWidget(QWidget):
    def __init__(self, map_filename, width, height, robot_width, robot_height):
        super().__init__()
        self.timer = QBasicTimer()
        self._width = width
        self._height = height
        self._robot_pixmap = QPixmap(robot_image_path)
        self._robot_width = robot_width
        self._robot_height = robot_height
        self._board_pixmap = QPixmap(width, height)
        self._board_pixmap.fill(QColor(0xffffff))
        self._label = QLabel()
        self._label.setPixmap(self._board_pixmap)
        self._layout = QVBoxLayout(self)
        self.initUI()

    def initUI(self):
        # self._label.setBackgroundRole(QPalette.Base)
        # self._label.setFixedSize(self._width, self._height)
        # self._label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self._label.setScaledContents(True)

        scroll = QScrollArea()
        scroll.setBackgroundRole(QPalette.Dark)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidget(self._label)
        scroll.setWidgetResizable(True)
        self._layout.addWidget(scroll)
        # self._layout.addWidget(self._label)
        self.setLayout(self._layout)
        # self.setMinimumSize(400, 400)
        self.setWindowTitle("Robot Emulator")

    def wheelEvent(self, event):
        pass

    def refresh(self):
        self._board_pixmap.fill(QColor(0xffffff))

    def draw_robot(self, top_left, angle):
        painter = QPainter(self._board_pixmap)
        xc, yc = top_left  # point to rotate around: top left corner
        painter.translate(xc, yc)
        painter.rotate(angle)
        # x, y = top_left
        x, y = 0, 0
        target = QRect(x, y, self._robot_width, self._robot_height)
        source = QRect(0., 0., self._robot_pixmap.width(), self._robot_pixmap.height())
        painter.drawPixmap(target, self._robot_pixmap, source)
        self._label.setPixmap(self._board_pixmap)
        painter.resetTransform()
        painter.end()

    def get_size(self):
        return self._width, self._height


# Joins control widget and the board
class MainView(QWidget):
    def __init__(self, map_filename, robot_width, robot_height):
        super().__init__()
        self._hscale_factor = 3
        self._vscale_factor = 3
        self._robot_width = robot_width * self._hscale_factor
        self._robot_height = robot_height * self._hscale_factor
        self._board_width = 400
        self._board_height = 400
        self._board_view = BoardWidget(map_filename, self._board_width, self._board_height,
                                       self._robot_width, self._robot_height)
        self._control = ControlWidget()
        self.initUI()
        self.show()

    def initUI(self):
        layout = QBoxLayout(QBoxLayout.RightToLeft, self)
        layout.addWidget(self._control)
        layout.addStretch(1)
        layout.addWidget(self._board_view)
        self.setLayout(layout)
        self.setWindowTitle('Robot Emulator')
        self.setWindowIcon(QIcon(robot_image_path))

    def _translate_y(self, point):
        x, y = point
        point = x, self._board_height - y
        return point

    @staticmethod
    def _translate_angle(angle):
        return -angle

    def draw_robot(self, left_top_pos, angle):
        self._board_view.refresh()
        left_top_pos = left_top_pos[0]*self._vscale_factor, left_top_pos[1]*self._hscale_factor
        self._board_view.draw_robot(self._translate_y(left_top_pos), self._translate_angle(angle))

    def set_left_forward_handler(self, handler):
        self._control.set_left_forward_handler(handler)

    def set_left_backward_handler(self, handler):
        self._control.set_left_backward_handler(handler)

    def set_right_forward_handler(self, handler):
        self._control.set_right_forward_handler(handler)

    def set_right_backward_handler(self, handler):
        self._control.set_right_backward_handler(handler)

    def set_both_forward_handler(self, handler):
        self._control.set_both_forward_handler(handler)

    def set_both_backward_handler(self, handler):
        self._control.set_both_backward_handler(handler)

    def set_left_power_changed_handler(self, handler):
        self._control.set_left_power_changed_handler(handler)

    def set_right_power_changed_handler(self, handler):
        self._control.set_right_power_changed_handler(handler)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = MainView("smth", 10, 8)
    b.draw_robot((0, 8), 0)
    b.show()
    sys.exit(app.exec_())