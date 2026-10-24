"""BFS that visits ALL destinations with the lowest cost."""

from all_common import start_node, is_goal, children, better, worth_exploring


def bfs_all(problem):
    """Return (cheapest complete route or None, nodes created).

    The first complete route BFS meets has the fewest moves, not the lowest
    cost, so the search continues and prunes branches costing at least as much
    as the best route found.
    """
    frontier = [start_node(problem)]
    created = 1
    best = None
    while frontier:
        current = frontier.pop(0)
        if not worth_exploring(current, best):
            continue
        if is_goal(problem, current):
            if better(current, best):
                best = current
            continue
        for child in children(problem, current):
            if worth_exploring(child, best):
                frontier.append(child)
                created += 1
    return best, created