"""Shared code for the research task: visit ALL destinations with the SHORTEST path.

A search state is (node ID, set of destinations visited so far). The goal is
reached when every destination has been visited. "Shortest" means lowest total
path cost. Loop avoidance forbids repeating the same STATE on one path (not
the same node), because the best route may have to pass through a node twice.
"""

import math


class VisitNode:
    """One node in the search tree, with the destinations visited so far."""

    def __init__(self, node_id, visited, parent=None, path_cost=0, moves=0):
        self.node_id = node_id
        self.visited = visited          # frozenset of destinations reached
        self.parent = parent
        self.path_cost = path_cost
        self.moves = moves

    def state(self):
        return (self.node_id, self.visited)

    def path(self):
        """Return this node's route from the origin as node IDs."""
        result, current = [], self
        while current is not None:
            result.append(current.node_id)
            current = current.parent
        result.reverse()
        return result

    def states_on_path(self):
        states, current = set(), self
        while current is not None:
            states.add(current.state())
            current = current.parent
        return states


def start_node(problem):
    """Root node; the origin counts as visited if it is a destination."""
    visited = frozenset([problem.origin]) if problem.origin in problem.destinations else frozenset()
    return VisitNode(problem.origin, visited)


def is_goal(problem, node):
    return len(node.visited) == len(problem.destinations)


def children(problem, node):
    """Children in ascending ID order, skipping states already on the path."""
    on_path = node.states_on_path()
    result = []
    for child_id, cost in problem.edges.get(node.node_id, []):
        visited = node.visited
        if child_id in problem.destinations:
            visited = visited | {child_id}
        if (child_id, visited) in on_path:
            continue
        result.append(VisitNode(child_id, visited, node, node.path_cost + cost, node.moves + 1))
    return result


def better(candidate, best):
    """True if candidate is a cheaper complete route than best."""
    return best is None or candidate.path_cost < best.path_cost


def worth_exploring(node, best):
    """Branch and bound: a node that already costs as much as best cannot improve it."""
    return best is None or node.path_cost < best.path_cost


def _distance(problem, a, b):
    ax, ay = problem.coordinates[a]
    bx, by = problem.coordinates[b]
    return math.hypot(ax - bx, ay - by)


def cost_scale(problem):
    """Smallest cost/length ratio over all edges, capped at 1.

    Multiplying straight-line distance by this keeps the heuristic admissible
    even when a road costs less than its straight-line length.
    """
    ratio = 1.0
    for a, neighbours in problem.edges.items():
        for b, cost in neighbours:
            length = _distance(problem, a, b)
            if length > 0:
                ratio = min(ratio, cost / length)
    return ratio


def make_heuristic(problem):
    """Lower bound on the remaining cost: farthest unvisited destination."""
    scale = cost_scale(problem)

    def h(node):
        remaining = [d for d in problem.destinations if d not in node.visited]
        if not remaining:
            return 0
        return scale * max(_distance(problem, node.node_id, d) for d in remaining)
    return h