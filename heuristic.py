"""Heuristics for tree-based search."""

import math


def nearest_destination_distance(problem, node_id):
    """Return the Euclidean distance to the nearest destination."""
    x, y = problem.coordinates[node_id]
    return min(
        math.hypot(x - problem.coordinates[destination][0], y - problem.coordinates[destination][1])
        for destination in problem.destinations
    )

def longest_edge_length(problem):
    """Return the longest straight-line length of any edge in the graph."""
    longest = 0.0
    for from_id, neighbours in problem.edges.items():
        from_x, from_y = problem.coordinates[from_id]
        for to_id, _ in neighbours:
            to_x, to_y = problem.coordinates[to_id]
            longest = max(longest, math.hypot(from_x - to_x, from_y - to_y))
    return longest


def moves_heuristic(problem, node_id, longest_edge):
    """Return a lower bound on the number of moves to the nearest destination.

    One move covers at most `longest_edge` in a straight line, so at least
    (distance / longest_edge) moves are needed. This never overestimates,
    so it is admissible for counting moves.
    """
    if longest_edge == 0:
        return 0
    distance = nearest_destination_distance(problem, node_id)
    # The tiny subtraction stops floating-point error from rounding up.
    return math.ceil(distance / longest_edge - 1e-9)