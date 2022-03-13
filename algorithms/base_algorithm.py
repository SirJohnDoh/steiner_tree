from typing import List, Tuple

from graph.graph import Edge, Vertex


class TreeSpanningAlgorithm:

    class Meta:
        abstract = True

    def __init__(self, terminal_vertices: List[Vertex], optional_vertices: List[Vertex]):
        self.terminal_vertices = terminal_vertices
        self.optional_vertices = optional_vertices

    def solve(self) -> Tuple[List[Edge], float]:
        raise NotImplementedError()
