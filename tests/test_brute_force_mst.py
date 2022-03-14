import pytest
from math import sqrt

from graph.graph import Vertex
from algorithms.brute_force_mst import BruteForceMST

from tests.utils import make_edges


@pytest.mark.parametrize(
    'vertices,expected_total_cost,expected_edge_indices',
    [
        # Empty or single vertex graph, no cost or edges
        ([], 0, []),
        ([Vertex(1, 1)], 0, []),
        # Two vertices should be conntected
        ([Vertex(0, 0), Vertex(0, 1), ], 1, [(0, 1)]),
        # Three vertices, connect both with the first node
        ([Vertex(0, 0), Vertex(0, 1), Vertex(1, 0)], 2, [(0, 1), (0, 2)]),
    ]
)
def test_no_optional(vertices, expected_total_cost, expected_edge_indices):

    expected_edges = make_edges(vertices, expected_edge_indices)

    edges, total_cost = BruteForceMST(vertices, []).solve()

    assert expected_total_cost == total_cost
    assert edges == expected_edges


@pytest.mark.parametrize(
    'vertices,optional_vertices,expected_total_cost,expected_edge_indices',
    [
        # Four vertices, connet through optional node in the middle
        (
            [Vertex(0, 0), Vertex(0, 1), Vertex(1, 0), Vertex(1, 1)],
            [Vertex(0.5, 0.5)],
            sqrt(0.5)*4,
            # 4 is the optional vertex
            [(0, 4), (1, 4), (2, 4), (3, 4)],
        ),
    ]
)
def test_with_optional_vertices(vertices, optional_vertices, expected_total_cost, expected_edge_indices):

    expected_edges = make_edges(vertices + optional_vertices, expected_edge_indices)

    edges, total_cost = BruteForceMST(vertices, optional_vertices).solve()

    assert expected_total_cost == total_cost
    # compare with set, order of edges does not matter for the solution
    assert set(edges) == set(expected_edges)
