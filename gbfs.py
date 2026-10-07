"""Greedy Best-First Search for a tree-based route-finding problem."""

from node import Node
import math


def heuristic(node_id, problem):
    """Return the heuristic value from a node to the closest destination."""
    x, y = problem.coordinates[node_id]

    return min(
        math.sqrt(
            (x - problem.coordinates[goal_id][0]) ** 2
            + (y - problem.coordinates[goal_id][1]) ** 2
        )
        for goal_id in problem.destinations
    )


def greedy_best_first(problem):
    """Return the first goal node found and the number of Nodes created."""
    origin_x, origin_y = problem.coordinates[problem.origin]

    frontier = [
        Node(problem.origin, origin_x, origin_y)
    ]

    nodes_created = 1

    while frontier:

        # Select the node with the smallest heuristic value
        current = min(
            frontier,
            key=lambda node: heuristic(node.node_id, problem)
        )

        frontier.remove(current)

        # Check whether the current node is a goal
        if current.node_id in problem.destinations:
            return current, nodes_created

        # Get nodes already in the current path
        path_ids = set(current.path())

        # Find valid children
        children = [
            (child_id, cost)
            for child_id, cost in problem.edges.get(current.node_id, [])
            if child_id not in path_ids
        ]

        # Add children to the frontier
        for child_id, cost in children:
            child_x, child_y = problem.coordinates[child_id]

            frontier.append(
                Node(
                    child_id,
                    child_x,
                    child_y,
                    parent=current,
                    path_cost=current.path_cost + cost,
                )
            )

            nodes_created += 1

    return None, nodes_created