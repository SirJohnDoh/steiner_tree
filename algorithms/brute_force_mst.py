import math
from typing import List

from itertools import chain, combinations

from algorithms.base_algorithm import TreeSpanningAlgorithm
from algorithms.minimum_spanning_tree import MinimumSpanningTree
from graph.graph import Vertex


def powerset(iteratble):
    s = list(iteratble)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class BruteForceMST(TreeSpanningAlgorithm):

    def __init__(self, terminal_vertices: List[Vertex], optional_vertices: List[Vertex]):
        super().__init__(terminal_vertices, optional_vertices)

    def solve(self):
        if not self.optional_vertices:
            return MinimumSpanningTree(self.terminal_vertices).solve()
        lowest_cost = math.inf
        best_solution = None

        for permutation in self.all_length_permutations():
            permuation_terminals = self.terminal_vertices + list(permutation)
            solution, solution_cost = MinimumSpanningTree(permuation_terminals).solve()
            if solution_cost < lowest_cost:
                lowest_cost = solution_cost
                best_solution = solution

        return (best_solution, lowest_cost)

    def all_length_permutations(self):
        for permutation in powerset(self.optional_vertices):
            yield permutation
