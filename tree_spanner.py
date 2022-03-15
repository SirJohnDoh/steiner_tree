#!env/bin/python

import argparse
import random

from datetime import datetime
from algorithms.brute_force_mst import BruteForceMST

from algorithms.dreyfus_wagner import DreyfusWagnerAlgorithm
from algorithms.minimum_spanning_tree import MinimumSpanningTree
from graph.graph import Vertex, eculidean_distance


def pick_algorithm(algorithm):
    if algorithm == 'dfw':
        return DreyfusWagnerAlgorithm
    if algorithm == 'mst':
        return MinimumSpanningTree
    if algorithm == 'bfmst':
        return BruteForceMST
    raise Exception(f'Unknown algorithm {algorithm}')


def pick_distance_function(distance_function):
    if distance_function == 'euclidian':
        return eculidean_distance
    raise Exception(f'Unknown distance function {distance_function}')


def randomize_terms_and_vertices(
    terminal_count,
    verticies_count,
    xmin,
    xmax,
    ymin,
    ymax,
):
    def rand_vert():
        return Vertex(random.uniform(xmin, xmax), random.uniform(ymin, ymax))

    terminals = [
        rand_vert() for i in range(terminal_count)
    ]
    vertices = [
        rand_vert() for i in range(verticies_count)
    ]
    return terminals, vertices


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '---algorithm',
        default='mst',
        help='The algorithm to run Dreyfus Wagner (dwf), Minimum Spanning tree (mst). Default mst',
        choices=['dfw', 'mst', 'bfmst'],
        type=str
    )
    parser.add_argument(
        '-d', '--distance_function',
        help='Function to calculate distance between vertices.',
        default='euclidian',
        choices=['euclidian'],
        type=str,
    )
    parser.add_argument(
        '-t', '--terminals',
        help='List of terminal vertices in the form of x1,y1 x2,y2 ... . For example 1.0,1.0 2.0,2.0',
        type=Vertex.from_str,
        nargs='+',
        default=[],
    )
    parser.add_argument(
        '-v', '--vertices',
        help='List of optional vertices, same format as terminals. Only used if the algorithm is Dreyfus Wagner.',
        type=Vertex.from_str,
        nargs='+',
        default=[],
    )
    parser.add_argument(
        '-r', '--random',
        help='Randomizes input terminals and optional verticies',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--tcount',
        help='Number of terminals to randomize, use with -r',
        type=int,
        default=0,
    )
    parser.add_argument(
        '--vcount',
        help='Number of optional verticies to randomize, use with -r',
        type=int,
        default=0,
    )
    parser.add_argument(
        '--xmin',
        help='Minimum value of x-axis to randomize, use with -r',
        default=0.0,
    )
    parser.add_argument(
        '--xmax',
        help='Maximum value of x-axis to randomize, use with -r',
        default=10.0,
    )
    parser.add_argument(
        '--ymin',
        help='Minimum value of y-axis to randomize, use with -r',
        default=0.0,
    )
    parser.add_argument(
        '--ymax',
        help='Maximum value of y-axis to randomize, use with -r',
        default=10.0,
    )
    parser.add_argument(
        '--seed',
        help='Random seed to use',
        type=int,
        required=False,
    )
    parser.add_argument(
        '--time',
        help='Measure the time of the solution',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '-q', '--quiet',
        help='Supress output',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '-p', '--plottable',
        help='Outputs only x and y coordinates of the edges',
        action='store_true',
        default=False,
    )
    arguments = parser.parse_args()
    arguments.algorithm = pick_algorithm(arguments.algorithm)
    arguments.distance_function = pick_distance_function(arguments.distance_function)

    if arguments.random:
        if arguments.seed:
            random.seed(arguments.seed)

        arguments.terminals, arguments.vertices = randomize_terms_and_vertices(
            arguments.tcount,
            arguments.vcount,
            arguments.xmin,
            arguments.xmax,
            arguments.ymin,
            arguments.ymax,
        )

    # Setup the distance function of the verticis
    for vert in arguments.terminals + arguments.vertices:
        vert.distance_function = arguments.distance_function

    return arguments


if __name__ == '__main__':
    arguments = parse_arguments()

    if not (arguments.quiet or arguments.plottable):
        print(
            f'Tree to span has {len(arguments.terminals)} terminal(s) and '
            f'{len(arguments.vertices)} optional node(s).'
        )
        print(f'Solution is searched with: {arguments.algorithm.__name__}')

    mark = None
    if arguments.time:
        mark = datetime.now()

    edges, total_cost = arguments.algorithm(arguments.terminals, arguments.vertices).solve()

    if mark:
        time = datetime.now() - mark
        if not (arguments.quiet or arguments.plottable):
            print(f'Solution took {time.total_seconds()} s')

    if not (arguments.quiet or arguments.plottable):
        print('Edges:')
        for e in edges:
            print(f'\t{e}')

        print(f'Total edge length: {total_cost:.2f}')

    if arguments.plottable:
        print(arguments.algorithm.__name__)
        print(total_cost)

        for terminal in arguments.terminals:
            print(f'{terminal.x},{terminal.y}')
        print()  # line feed

        for vertices in arguments.vertices:
            print(f'{vertices.x},{vertices.y}')
        print()  # line feed

        for e in edges:
            print(f'{e.v1.x},{e.v1.y};{e.v2.x},{e.v2.y}')
        print()  # line feed
