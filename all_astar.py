"""A* search that visits ALL destinations with the lowest cost."""

import heapq

from all_common import start_node, is_goal, children, make_heuristic


def astar_all(problem):
    """Return (cheapest complete route or None, nodes created).

    f = g + h with an admissible h (see all_common.make_heuristic), so the first
    complete route taken from the frontier is the cheapest.
    """
    h = make_heuristic(problem)
    origin = start_node(problem)
    counter = 0
    frontier = [(h(origin), origin.node_id, counter, origin)]
    created = 1
    while frontier:
        _, _, _, current = heapq.heappop(frontier)
        if is_goal(problem, current):
            return current, created
        for child in children(problem, current):
            counter += 1
            heapq.heappush(frontier, (child.path_cost + h(child), child.node_id, counter, child))
            created += 1
    return None, created