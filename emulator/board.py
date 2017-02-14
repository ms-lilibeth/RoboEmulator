import numpy as np


# Behaves like a model. Contains info about the maze in standard units
class Board:
    def __init__(self, filename=None):
        self._maze = None
        self._width = 0
        self._height = 0
        if filename is not None:
            self.from_file(filename)

    def from_file(self, filename):
        self._width = 400
        self._height = 400
        # TODO

    #  Checks if a square object intersects with walls of a maze
    def has_collisions(self, top_left, bottom_right):
        # TODO
        return False

    def get_data(self):
        # TODO
        return None
        # return self._maze[:, :]
