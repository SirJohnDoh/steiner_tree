from graph.graph import Edge


def make_edges(vertices, edge_indices):
    return [
        Edge(vertices[i], vertices[j]) for i, j in edge_indices
    ]
