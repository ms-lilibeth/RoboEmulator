# from robot import Robot
# from interface import EmulatorWidget
# from board import Board
from emulator.robot import Robot
from emulator.interface import MainView
from emulator.board import Board


class Emulator:
    def __init__(self, robot, board):
        self._robot = robot
        self._board = board
        self._view = MainView()

    # update view on timer

