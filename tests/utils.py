from graph.graph import Edge


def make_edges(verticies, edge_indicies):
    return [
        Edge(verticies[i], verticies[j]) for i, j in edge_indicies
    ]
