import pytest

from math import sqrt

from graph.graph import Vertex, Edge


@pytest.mark.parametrize(
    'v1,v2,expected_distance',
    [
        (Vertex(0, 0), Vertex(1, 0), 1.0),
        (Vertex(0, 0), Vertex(0, 1), 1.0),
        (Vertex(0, 0), Vertex(1, 1), sqrt(2)),
    ]
)
def test_vertex_distance(v1, v2, expected_distance):
    assert v1.distance_to(v2) == v2.distance_to(v1) == expected_distance


@pytest.mark.parametrize(
    'edge,expected_distance',
    [
        (Edge(Vertex(0, 0), Vertex(1, 0)), 1.0),
        (Edge(Vertex(0, 0), Vertex(0, 1)), 1.0),
        (Edge(Vertex(0, 0), Vertex(1, 1)), sqrt(2)),
    ]
)
def test_edge_distance(edge, expected_distance):
    assert edge.distance() == expected_distance


@pytest.mark.parametrize(
    'edges,expected_order',
    [
        (
            [
                Edge(Vertex(0, 0), Vertex(1, 1)),
                Edge(Vertex(0, 0), Vertex(1, 0)),
                Edge(Vertex(0, 0), Vertex(0, 1)),
                Edge(Vertex(0, 0), Vertex(0, 0)),
            ],
            [
                Edge(Vertex(0, 0), Vertex(0, 0)),
                # Stable sort, this should be after the one with same distance
                Edge(Vertex(0, 0), Vertex(1, 0)),
                Edge(Vertex(0, 0), Vertex(0, 1)),
                Edge(Vertex(0, 0), Vertex(1, 1)),
            ],
        ),
    ]
)
def test_order_edges(edges, expected_order):
    assert sorted(edges) == expected_order


@pytest.mark.parametrize(
    'e1,e2',
    [
        # Order of vertices should not matter
        (Edge(Vertex(0, 0), Vertex(1, 0)), Edge(Vertex(1, 0), Vertex(0, 0))),
    ]
)
def test_edge_equals(e1, e2):
    assert e1 == e2
