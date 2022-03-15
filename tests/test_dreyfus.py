import pytest
from math import sqrt

from graph.graph import Vertex
from algorithms.dreyfus_wagner import DreyfusWagnerAlgorithm

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

    edges, total_cost = DreyfusWagnerAlgorithm(vertices, []).solve()

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
        # Randomized test found failing during implementation, uses no optional verticies
        (
            [
                Vertex(1.46, 4.55), Vertex(7.71, 7.06), Vertex(7.32, 4.34), Vertex(8.00, 5.33), Vertex(0.80, 4.56),
                Vertex(0.48, 9.33), Vertex(9.47, 3.35), Vertex(3.09, 7.68), Vertex(2.04, 1.78), Vertex(1.89, 3.47)],
            [
                Vertex(6.26, 9.63), Vertex(2.11, 9.56), Vertex(5.55, 9.01), Vertex(8.18, 1.60), Vertex(6.49, 1.24),
                Vertex(0.06, 3.96), Vertex(7.74, 5.66), Vertex(1.93, 8.41), Vertex(9.14, 2.37), Vertex(4.48, 6.38)
            ],
            20.119559224905053,
            [(0, 4), (0, 9), (8, 9), (0, 7), (5, 7), (7, 1), (1, 3), (2, 3), (2, 6)],
        )
    ]
)
def test_with_optional_vertices(vertices, optional_vertices, expected_total_cost, expected_edge_indices):

    expected_edges = make_edges(vertices + optional_vertices, expected_edge_indices)

    edges, total_cost = DreyfusWagnerAlgorithm(vertices, optional_vertices).solve()

    assert expected_total_cost == total_cost
    # Order should not matter
    assert set(edges) == set(expected_edges)
