import pytest

from algorithms.minimum_spanning_tree import MinimumSpanningTree
from graph.graph import Vertex


@pytest.mark.parametrize(
    'verticies,expected_total_cost,expected_edges',
    [
        # Empty or single vertex graph, no cost or edges
        ([], 0, []),
        ([Vertex(1, 1)], 0, []),
    ]
)
def test(verticies, expected_total_cost, expected_edges):

    edges, total_cost = MinimumSpanningTree(verticies).solve()

    assert edges == expected_edges
    assert total_cost == expected_total_cost
