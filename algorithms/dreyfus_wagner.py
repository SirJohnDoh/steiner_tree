from bitarray import bitarray
from typing import List, Tuple

from algorithms.base_algorithm import TreeSpanningAlgorithm
from graph.graph import Edge, Vertex


# A class used in a map to save search states during the algorithm
class SearchState:
    def __init__(self, vertex: Vertex, remaining: bitarray):
        self.vertex = vertex
        self.remaining = remaining

    def __eq__(self, other):
        return other and self.vertex == other.vertex and self.remaining == other.remaining

    def __hash__(self):
        # Maybe not that efficient way to calculate a hash value
        return hash(self.vertex) + 37 * hash(self.remaining.to01())

    def __repr__(self):
        return 'V: ' + self.vertex.__repr__() + ' remaining: ' + self.remaining.__repr__()


class DreyfusWagnerAlgorithm(TreeSpanningAlgorithm):

    def __init__(self, terminal_vertices: List[Vertex], optional_vertices: List[Vertex]):
        super().__init__(terminal_vertices, optional_vertices)
        self.split_map = dict()
        self.candidate_map = dict()
        self._total_cost = 0.0
        self.steiner_edges = []
        self.steiner_vertices = []
        self.terminal_to_index = dict()

    def solve(self) -> Tuple[List[Edge], float]:

        # No verticies
        if not self.terminal_vertices:
            return [], 0.0

        remaining = bitarray(len(self.terminal_vertices))
        remaining.setall(True)

        # Create a mapping of a terminal vertex to its index in the list
        for i in range(len(self.terminal_vertices)):
            self.terminal_to_index[self.terminal_vertices[i]] = i

        # Start at the first terminal
        remaining[0] = False

        self._total_cost = self._connect_vertex(self.terminal_vertices[0], remaining)
        self._build_solution_connect(self.terminal_vertices[0], remaining)

        return self.steiner_edges, self.total_cost()

    def total_cost(self) -> float:
        return self._total_cost

    def _connect_vertex(self, vertex: List[Vertex], remaining_terminals: bitarray) -> float:

        # Copy the remaining terminals
        remaining = bitarray(remaining_terminals)

        remaining_count = remaining.count()  # Count number of 1's in the array

        if (remaining_count == 0):  # Every terminal is accounted for, terminate recursion
            return 0

        if (remaining_count == 1):  # Only one terminal left
            # Find the index of that terminal
            index = remaining.index(True)

            # Look up distance between the remaining terminal and the current vertex
            distance = vertex.distance_to(self.terminal_vertices[index])

            # Add tuple of distance and the remaining vertex to the candidate map
            self.candidate_map[SearchState(vertex, remaining)] = (
                            distance, self.terminal_vertices[index]
                        )
            return distance

        # Try to get it or None
        existing_candidate = self.candidate_map.get(
                    SearchState(vertex, remaining),
                    None
                )
        if (existing_candidate is not None):
            return existing_candidate[0]  # Return the distance part of the tuple

        best_split_distance = self._split_vertex(vertex, remaining)
        candidate = vertex

        # Check every grid vertex if they can offer a better split
        for optional_vertex in self.optional_vertices:
            distance = self._split_vertex(optional_vertex, remaining)
            distance += vertex.distance_to(optional_vertex)
            if (best_split_distance < 0 or distance < best_split_distance):
                # Found a better split
                best_split_distance = distance
                candidate = optional_vertex

        for vert, index in self.terminal_to_index.items():
            if (not remaining[index]):  # Ignore any used terminal
                continue

            remaining[index] = False  # Set the terminal bit to false temporarily
            # Recursive call
            distance = self._connect_vertex(vert, remaining)

            distance += vertex.distance_to(vert)
            remaining[index] = True  # Set  it back

            if (best_split_distance < 0 or distance < best_split_distance):
                # Found a better split
                best_split_distance = distance
                candidate = vert

        # Add the new found best distance and the candidate vertex to the map
        self.candidate_map[SearchState(vertex, remaining)] = (
            best_split_distance,
            candidate
        )
        return best_split_distance

    def _split_vertex(self, vertex: Vertex, remaining_terminals: bitarray) -> float:

        # Copy the remaining terminals
        remaining = bitarray(remaining_terminals)

        if (remaining.count() < 2):  # No steiner vertex exists for less than 2 terminals
            return 0

        existing_split = self.split_map.get(SearchState(vertex, remaining), None)
        if (existing_split is not None):
            return existing_split[0]  # Return the distance

        # Find smallest index and add one to avoid checking the same subset twice
        index = remaining.index(True) + 1
        best = self._best_split(vertex, remaining, remaining, index)
        self.split_map[SearchState(vertex, remaining)] = best

        return best[0]  # Return the distance

    def _best_split(
        self,
        vertex: Vertex,
        remaining_terminals: bitarray,
        subset_terminals: bitarray,
        index: int
    ) -> float:

        # Copy the remaining and subset terminals bit arrays
        remaining = bitarray(remaining_terminals)
        subset = bitarray(subset_terminals)

        if (index == len(self.terminal_vertices)):  # Index is not a valid vertex in terminals
            complement = remaining ^ subset  # XOR of the two bit arrays
            if (subset.any() and complement.any()):  # If both have at least one bit set to 1

                # Two recursive calls
                d1 = self._connect_vertex(vertex, subset)  # Call the search on the subset
                d2 = (self._connect_vertex(vertex, complement))  # And its complement

                distance = d1 + d2
                # Returns the tuple of the distance and the tested subset of terminals
                return (distance, subset)
            else:
                return (-1, None)  # No split possible

        # Try to recursively find the best split
        result1 = self._best_split(vertex, remaining, subset, index + 1)
        if (remaining[index]):  # If the current index is a remaining terminal
            subset[index] = not subset[index]  # Flip the bit at index
            result2 = self._best_split(vertex, remaining, subset, index + 1)

            # If result 1 is a failed result or if the result 2 has lower distance use the second result
            if (result1[0] < 0 or result2[0] < result1[0]):
                result1 = result2

        return result1

    def _build_solution_connect(self, vertex: Vertex, remaining_terminals: bitarray) -> None:
        # Copy the remaining terminals
        remaining = bitarray(remaining_terminals)

        if (not remaining.any()):  # No terminals remaining
            return

        next_vertex = self.candidate_map[SearchState(vertex, remaining)][1]

        if (vertex == next_vertex):
            self._build_solution_split(next_vertex, remaining)
            return

        terminal_index = self.terminal_to_index.get(next_vertex, None)
        if (terminal_index is None):
            # Add the non-terminal vertex to the list of steiner vertices
            self.steiner_vertices += [next_vertex]
            # Add the edge from vertex to nextVertex to the list of edges
            self.steiner_edges.append(Edge(vertex, next_vertex))
            self._build_solution_split(next_vertex, remaining)
            return
        # Add the edge from vertex to the terminal vertex to the list of edges
        self.steiner_edges.append(Edge(vertex, next_vertex))

        # Flip the bit at terminalIndex
        remaining[terminal_index] = not remaining[terminal_index]
        self._build_solution_connect(next_vertex, remaining)

    def _build_solution_split(self, vertex: Vertex, remaining_terminals: bitarray) -> None:
        # Copy the remaining terminals
        remaining = bitarray(remaining_terminals)

        if (not remaining.any()):  # No terminals remaining
            return

        # Find the subset that was used when splitting
        split_subset = self.split_map[SearchState(vertex, remaining)][1]
        self._build_solution_connect(vertex, split_subset)
        self._build_solution_connect(vertex, remaining ^ split_subset)
