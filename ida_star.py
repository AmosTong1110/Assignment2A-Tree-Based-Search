"""Iterative Deepening A* search for the route-finding problem."""

import math

from node import Node
from heuristic import nearest_destination_distance


def ida_star(problem):
    """Return (goal Node or None, number of Nodes created)."""

    # Scale the distance heuristic so it cannot overestimate
    # remaining cost when edge costs are smaller than distances.
    scale = 1.0

    for source_id, neighbours in problem.edges.items():
        source_x, source_y = problem.coordinates[source_id]

        for target_id, cost in neighbours:
            if cost < 0:
                raise ValueError("IDA* requires non-negative edge costs")

            target_x, target_y = problem.coordinates[target_id]
            distance = math.hypot(
                target_x - source_x,
                target_y - source_y,
            )

            if distance > 0:
                scale = min(scale, cost / distance)

    def heuristic(node_id):
        return scale * nearest_destination_distance(problem, node_id)

    # Create the starting search-tree node.
    origin_x, origin_y = problem.coordinates[problem.origin]
    start = Node(problem.origin, origin_x, origin_y)

    nodes_created = 1
    threshold = heuristic(start.node_id)

    # Track only nodes on the current route to prevent cycles.
    path_ids = {start.node_id}

    def bounded_search(current, limit):
        """Return (goal or None, smallest exceeded f-value)."""
        nonlocal nodes_created

        f_value = current.path_cost + heuristic(current.node_id)

        # This route exceeds the current cost limit.
        if f_value > limit:
            return None, f_value

        # A destination has been reached within the limit.
        if current.node_id in problem.destinations:
            return current, math.inf

        next_threshold = math.inf

        # Explore neighbours in ascending node-ID order.
        neighbours = sorted(
            problem.edges.get(current.node_id, []),
            key=lambda edge: edge[0],
        )

        for child_id, edge_cost in neighbours:
            if child_id in path_ids:
                continue

            child_x, child_y = problem.coordinates[child_id]
            child = Node(
                child_id,
                child_x,
                child_y,
                parent=current,
                path_cost=current.path_cost + edge_cost,
            )
            nodes_created += 1

            path_ids.add(child_id)
            goal, exceeded_value = bounded_search(child, limit)
            path_ids.remove(child_id)

            if goal is not None:
                return goal, math.inf

            next_threshold = min(next_threshold, exceeded_value)

        return None, next_threshold

    # Repeat the depth-first search with increasing cost limits.
    while True:
        goal, next_threshold = bounded_search(start, threshold)

        if goal is not None:
            return goal, nodes_created

        # No goal and no remaining branch beyond the limit.
        if next_threshold == math.inf:
            return None, nodes_created

        threshold = next_threshold