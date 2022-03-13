import heapq
from graph.graph import Edge, Vertex
from typing import List, Tuple


class MinimumSpanningTree:

    def __init__(self, vertices: List[Vertex]):
        self.vertices = vertices
        self.edges = []
        self.heap_priorty_q = []
        self.start_vertex = self.vertices[0] if vertices else None

    def solve(self) -> Tuple[List[Edge], float]:
        # No verticies
        if not self.start_vertex:
            return self.edges, self.total_cost()

        visited = set()

        self._add_every_edge(self.start_vertex)
        visited.add(self.start_vertex)

        while len(self.heap_priorty_q) > 0 and len(visited) != len(self.vertices):
            next_edge = heapq.heappop(self.heap_priorty_q)

            # Skip any visited vertices
            if (next_edge.v2 in visited):
                continue
            # Add lowest edge to the tree
            self.edges += [next_edge]

            # Mark the next vertex as visited
            visited.add(next_edge.v2)

            # Add the edges from next vertex

            self._add_every_edge(next_edge.v2)

        return self.edges, self.total_cost()

    def total_cost(self):
        return sum(e.distance() for e in self.edges)

    def _add_every_edge(self, from_vertex):
        for vertex in self.vertices:
            if (vertex != from_vertex):
                e = Edge(from_vertex, vertex)
                heapq.heappush(self.heap_priorty_q, e)
