"""CUS1: iterative deepening DFS that visits ALL destinations with the lowest cost."""

from all_common import start_node, is_goal, children, better, worth_exploring


def depth_limited_all(problem, depth_limit, best):
    """DFS to depth_limit. Returns (best route so far, nodes created, cut off?)."""
    stack = [(start_node(problem), 0)]
    created = 1
    cutoff = False
    while stack:
        current, depth = stack.pop()
        if not worth_exploring(current, best):
            continue
        if is_goal(problem, current):
            if better(current, best):
                best = current
            continue
        kids = [c for c in children(problem, current) if worth_exploring(c, best)]
        if depth == depth_limit:
            if kids:
                cutoff = True
            continue
        for child in reversed(kids):
            stack.append((child, depth + 1))
            created += 1
    return best, created, cutoff


def iddfs_all(problem):
    """Return (cheapest complete route or None, nodes created over all rounds).

    The first round that finds a route gives the fewest moves, not the lowest
    cost, so deepening continues until no branch is cut off by the limit.
    """
    created = 0
    depth_limit = 0
    best = None
    while True:
        best, made, cutoff = depth_limited_all(problem, depth_limit, best)
        created += made
        if not cutoff:
            return best, created
        depth_limit += 1