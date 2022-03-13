#!env/bin/python

from matplotlib import pyplot
import sys


def plot_str_coords(coords: str, opts: str = None):
    x, y = coords.split(',')
    pyplot.plot(float(x), float(y), opts)


def plot_line(coord1, coord2: str, opts: str = None):
    x1, y1 = coord1.split(',')
    x2, y2 = coord2.split(',')
    pyplot.plot([float(x1), float(x2)], [float(y1), float(y2)], opts)


name = sys.stdin.readline()
total_distance = float(sys.stdin.readline())

pyplot.title(f'{name}\ntotal distance: {total_distance:.2f}')

for line in sys.stdin:
    if not line.strip():
        break
    plot_str_coords(line, 'bo')


for line in sys.stdin:
    if not line.strip():
        break

    plot_str_coords(line, 'ro')


for line in sys.stdin:
    if not line.strip():
        break

    v1, v2 = line.split(';')
    plot_line(v1, v2, 'b-')


pyplot.show()
