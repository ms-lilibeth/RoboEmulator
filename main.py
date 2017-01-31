from mapGenerator.maze_generator import generate_in_standard_units
from mapGenerator.maze_generator import _print_raw, _generate_Euler
import scipy.misc

# width = 20
# height = 20
# pass_width = 2
# border_width = 1
#
# maze = _generate_Euler(10, 10)
# _print_raw(maze)
# exit()
width = 990
height = 900
pass_width = 35  # min -- 16
border_width = 6

maze = generate_in_standard_units(width, height, pass_width, border_width, filename_out="maze.txt")

scipy.misc.imsave('maze.png', maze)
