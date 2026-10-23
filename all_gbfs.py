"""Greedy best-first search that visits ALL destinations with the lowest cost."""

import heapq

from all_common import start_node, is_goal, children, better, worth_exploring, make_heuristic


def gbfs_all(problem):
    """Return (cheapest complete route or None, nodes created).

    Nodes are picked by heuristic only (ties: smaller ID, then older node).
    Greedy order does not guarantee the cheapest route, so the search keeps
    going after the first complete route and prunes by the best cost found.
    """
    h = make_heuristic(problem)
    origin = start_node(problem)
    counter = 0
    frontier = [(h(origin), origin.node_id, counter, origin)]
    created = 1
    best = None
    while frontier:
        _, _, _, current = heapq.heappop(frontier)
        if not worth_exploring(current, best):
            continue
        if is_goal(problem, current):
            if better(current, best):
                best = current
            continue
        for child in children(problem, current):
            if worth_exploring(child, best):
                counter += 1
                heapq.heappush(frontier, (h(child), child.node_id, counter, child))
                created += 1
    return best, created