import pytest

from algorithms.minimum_spanning_tree import MinimumSpanningTree
from graph.graph import Edge, Vertex


def make_edges(verticies, edge_indicies):
    return [
        Edge(verticies[i], verticies[j]) for i, j in edge_indicies
    ]


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
def test(verticies, expected_total_cost, expected_edge_indices):

    expected_edges = make_edges(verticies, expected_edge_indices)

    edges, total_cost = MinimumSpanningTree(verticies).solve()

    assert edges == expected_edges
    assert total_cost == expected_total_cost
