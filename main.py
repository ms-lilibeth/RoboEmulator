from mapGenerator.maze_generator import generate_in_standard_units
from mapGenerator.maze_generator import _print_raw, _generate_Euler
import png

# width = 150
# height = 150
# pass_width = 16
# border_width = 4
width = 20
height = 20
pass_width = 2
border_width = 1

maze = _generate_Euler(10, 10)
_print_raw(maze)
exit()

maze = generate_in_standard_units(width, height, pass_width, border_width)
with open("maze.txt", 'w') as f:
    for row in maze:
        for i in row:
            f.write(str(i) + " ")
        f.write("\n")

pngWriter = png.Writer(width=width, height=height, greyscale=True)
with open("maze.png", 'wb') as f:
    pngWriter.write(f, maze)
