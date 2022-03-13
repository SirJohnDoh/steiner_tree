import pytest

from algorithms.minimum_spanning_tree import MinimumSpanningTree
from graph.graph import Vertex
from tests.utils import make_edges


@pytest.mark.parametrize(
    'vertices,expected_total_cost,expected_edge_indices',
    [
        # Empty or single vertex graph, no cost or edges
        ([], 0, []),
        ([Vertex(1, 1)], 0, []),
        # Two vertices should be conntected
        ([Vertex(0, 0), Vertex(0, 1)], 1, [(0, 1)]),
        # Three vertices, connect both with the first node
        ([Vertex(0, 0), Vertex(0, 1), Vertex(1, 0)], 2, [(0, 1), (0, 2)]),
    ]
)
def test(vertices, expected_total_cost, expected_edge_indices):

    expected_edges = make_edges(vertices, expected_edge_indices)

    edges, total_cost = MinimumSpanningTree(vertices).solve()

    assert edges == expected_edges
    assert total_cost == expected_total_cost
