from robot import Robot
from interface import MainView
from board import Board
# from emulator.robot import Robot
# from emulator.interface import MainView
# from emulator.board import Board
from PyQt5.QtCore import QTimer


class Emulator:
    def __init__(self, map_filename):
        self._robot = Robot()
        self._board = Board(map_filename)
        self._view = MainView(map_filename, self._robot.width, self._robot.height)
        self._timer = QTimer()
        self._timer.timeout.connect(self._update)
        self._connect_buttons()

        self._stuck = {"LF": False, "LB": False, "RF": False, "RB": False, "BF": False, "BB": False}
        self._timer.start(100)

    def _connect_buttons(self):
        self._view.set_left_forward_handler(self._left_forward)
        self._view.set_left_backward_handler(self._left_backward)
        self._view.set_right_forward_handler(self._right_forward)
        self._view.set_right_backward_handler(self._right_backward)
        self._view.set_both_forward_handler(self._both_forward)
        self._view.set_both_backward_handler(self._both_backward)

    def _clear_stuck_flags(self):
        self._stuck = {"LF": False, "LB": False, "RF": False, "RB": False, "BF": False, "BB": False}

    def _update(self):
        pos, angle = self._robot.get_state()
        self._view.draw_robot(pos, angle)

    def _left_forward(self):
        if self._stuck["LF"]:
            return
        top_left, angle = self._robot.left_engine_forward()
        if self._board.has_collisions(top_left, angle):
            self._clear_stuck_flags()
            self._stuck["LF"] = True
        else:
            self._robot.set_state(top_left, angle)

    def _left_backward(self):
        if self._stuck["LB"]:
            return
        top_left, angle = self._robot.left_engine_backward()
        if self._board.has_collisions(top_left, angle):
            self._clear_stuck_flags()
            self._stuck["LB"] = True
        else:
            self._robot.set_state(top_left, angle)

    def _right_forward(self):
        if self._stuck["RF"]:
            return
        top_left, angle = self._robot.right_engine_forward()
        if self._board.has_collisions(top_left, angle):
            self._clear_stuck_flags()
            self._stuck["RF"] = True
        else:
            self._robot.set_state(top_left, angle)

    def _right_backward(self):
        if self._stuck["RB"]:
            return
        top_left, angle = self._robot.right_engine_backward()
        if self._board.has_collisions(top_left, angle):
            self._clear_stuck_flags()
            self._stuck["RB"] = True
        else:
            self._robot.set_state(top_left, angle)

    def _both_forward(self):
        if self._stuck["BF"]:
            return
        top_left, angle = self._robot.both_engines_forward()
        if self._board.has_collisions(top_left, angle):
            self._clear_stuck_flags()
            self._stuck["BF"] = True
        else:
            self._robot.set_state(top_left, angle)

    def _both_backward(self):
        if self._stuck["BB"]:
            return
        top_left, angle = self._robot.both_engines_backward()
        if self._board.has_collisions(top_left, angle):
            self._clear_stuck_flags()
            self._stuck["BB"] = True
        else:
            self._robot.set_state(top_left, angle)