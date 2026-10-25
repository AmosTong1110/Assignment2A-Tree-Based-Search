"""CUS2: iterative deepening A* that visits ALL destinations with the lowest cost."""

import math

from all_common import start_node, is_goal, children, make_heuristic

EPSILON = 1e-9   # avoids floating-point error when comparing f-values


def ida_star_all(problem):
    """Return (cheapest complete route or None, nodes created over all rounds).

    Here f = g + h is measured in COST (the main program's CUS2 uses moves).
    With an admissible h, the first complete route inside the threshold is the
    cheapest. The threshold rises to the smallest f-value that was exceeded.
    """
    h = make_heuristic(problem)
    start = start_node(problem)
    created = 0
    threshold = h(start)

    def bounded_search(current, limit):
        nonlocal created
        f_value = current.path_cost + h(current)
        if f_value > limit + EPSILON:
            return None, f_value
        if is_goal(problem, current):
            return current, math.inf
        next_threshold = math.inf
        for child in children(problem, current):
            created += 1
            goal, exceeded = bounded_search(child, limit)
            if goal is not None:
                return goal, math.inf
            next_threshold = min(next_threshold, exceeded)
        return None, next_threshold

    while True:
        created += 1
        goal, next_threshold = bounded_search(start, threshold)
        if goal is not None:
            return goal, created
        if next_threshold == math.inf:
            return None, created
        threshold = next_threshold