import pytest

from graph.graph import Vertex
from algorithms.dreyfus_wagner import DreyfusWagnerAlgorithm

from tests.utils import make_edges


@pytest.mark.parametrize(
    'verticies,expected_total_cost,expected_edge_indices',
    [
        # Empty or single vertex graph, no cost or edges
        ([], 0, []),
        ([Vertex(1, 1)], 0, []),
        # Two verticies should be conntected
        ([Vertex(0, 0), Vertex(0, 1), ], 1, [(0, 1)]),
        # Three verticies, connect both with the first node
        ([Vertex(0, 0), Vertex(0, 1), Vertex(1, 0)], 2, [(0, 1), (0, 2)]),
    ]
)
def test_no_optional(verticies, expected_total_cost, expected_edge_indices):

    expected_edges = make_edges(verticies, expected_edge_indices)

    edges, total_cost = DreyfusWagnerAlgorithm(verticies, []).solve()

    assert expected_total_cost == total_cost
    assert edges == expected_edges
