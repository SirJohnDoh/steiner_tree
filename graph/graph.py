from __future__ import annotations

from functools import total_ordering
from math import sqrt
from typing import Callable


def eculidean_distance(v1, v2):
    x2 = pow(v2.x - v1.x, 2)
    y2 = pow(v2.y - v1.y, 2)
    return sqrt(x2 + y2)


class Vertex:

    @classmethod
    def from_str(cls, vertex_str: str, distance_function: Callable[[Vertex, Vertex], float] = eculidean_distance):
        x, y = vertex_str.split(',')
        x = float(x)
        y = float(y)
        return cls(x, y, distance_function)

    def __init__(self, x, y, distance_function: Callable[[Vertex, Vertex], float] = eculidean_distance):
        self.x = x
        self.y = y
        self.distance_function = distance_function

    def distance_to(self, other: Vertex):
        return self.distance_function(self, other)

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) + 37 * hash(self.y)

    def __getitem__(self, key):
        if (key == 0):
            return self.x
        return self.y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.x:.2f},{self.y:.2f})"


@total_ordering
class Edge:
    def __init__(self, v1: Vertex, v2: Vertex):
        self.v1 = v1
        self.v2 = v2

    def distance(self):
        return self.v1.distance_to(self.v2)

    def __lt__(self, other: Edge):
        return self.distance() < other.distance()

    def __eq__(self, other: Edge):
        return (
            self.distance() == other.distance() and
            # Edges are omnidirectional
            (
                self.v1 == other.v1 and
                self.v2 == other.v2
            ) or
            (
                self.v1 == other.v2 and
                self.v2 == other.v1
            )
        )

    def __str__(self):
        return f'{self.v1} <-> {self.v2}'
