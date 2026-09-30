"""Heuristics for tree-based search."""

import math


def nearest_destination_distance(problem, node_id):
    """Return the Euclidean distance to the nearest destination."""
    x, y = problem.coordinates[node_id]
    return min(
        math.hypot(x - problem.coordinates[destination][0], y - problem.coordinates[destination][1])
        for destination in problem.destinations
    )
