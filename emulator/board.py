import numpy as np


# Behaves like a model. Contains info about the maze in standard units
class Board:
    def __init__(self, filename=None):
        self._maze = None
        if filename is not None:
            self.from_file(filename)

    def from_file(self, filename):
        pass

    #  Checks if a square object intersects with walls of a maze
    def has_collisions(self, left_top, right_top, right_bottom, left_bottom):
        pass

    def get_data(self):
        return self._maze[:, :]
