"""Run a tree-based search method on a problem file."""

import sys

from dfs import dfs
from ida_star import ida_star
from problem import load_problem


SEARCH_METHODS = {
    "DFS": dfs,
    "BFS": None,
    "GBFS": None,
    "AS": None,
    "CUS1": None,
    "CUS2": ida_star,
}


def main():
    """Parse command-line arguments, run DFS, and print the required output."""
    if len(sys.argv) != 3:
        print("Usage: python search.py <filename> <method>")
        return 1

    filename = sys.argv[1]
    method = sys.argv[2]

    method_name = method.upper()
    if method_name not in SEARCH_METHODS:
        print(f"Unknown method: {method}")
        return 1

    if SEARCH_METHODS[method_name] is None:
        print(f"{method_name} is not implemented yet")
        return 0

    try:
        problem = load_problem(filename)
    except OSError as error:
        print(f"Could not read file '{filename}': {error}")
        return 1
    except ValueError as error:
        print(error)
        return 1

    goal, nodes_created = SEARCH_METHODS[method_name](problem)

    print(f"{filename} {method}")
    if goal is None:
        print(f"None {nodes_created}")
        print()
    else:
        print(f"{goal.node_id} {nodes_created}")
        print(" ".join(str(node_id) for node_id in goal.path()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
