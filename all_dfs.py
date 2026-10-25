"""DFS (branch and bound) that visits ALL destinations with the lowest cost."""

from all_common import start_node, is_goal, children, better, worth_exploring


def dfs_all(problem):
    """Return (cheapest complete route or None, nodes created).

    Plain DFS stops at the first complete route, which may be expensive. Here it
    keeps going and only abandons branches that already cost as much as the best.
    """
    frontier = [start_node(problem)]
    created = 1
    best = None
    while frontier:
        current = frontier.pop()
        if not worth_exploring(current, best):
            continue
        if is_goal(problem, current):
            if better(current, best):
                best = current
            continue
        for child in reversed(children(problem, current)):
            if worth_exploring(child, best):
                frontier.append(child)
                created += 1
    return best, created