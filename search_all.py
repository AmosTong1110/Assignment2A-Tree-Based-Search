"""Research mode: visit ALL destinations with the shortest path.

Usage: python search_all.py <filename> <method>
"""

import sys

from all_astar import astar_all
from all_bfs import bfs_all
from all_dfs import dfs_all
from all_gbfs import gbfs_all
from all_ida_star import ida_star_all
from all_iddfs import iddfs_all
from problem import load_problem

SEARCH_METHODS = {
    "DFS": dfs_all,
    "BFS": bfs_all,
    "GBFS": gbfs_all,
    "AS": astar_all,
    "CUS1": iddfs_all,
    "CUS2": ida_star_all,
}


def main():
    """Parse arguments, run the chosen method, and print the required output."""
    if len(sys.argv) != 3:
        print("Usage: python search_all.py <filename> <method>")
        return 1
    filename = sys.argv[1]
    method_name = sys.argv[2].upper()
    if method_name not in SEARCH_METHODS:
        print(f"Unknown method: {sys.argv[2]}")
        return 1
    try:
        problem = load_problem(filename)
    except (OSError, ValueError) as error:
        print(error)
        return 1

    goal, nodes_created = SEARCH_METHODS[method_name](problem)
    print(f"{filename} {method_name}")
    if goal is None:
        print(f"None {nodes_created}")
        print()
    else:
        print(f"{goal.node_id} {nodes_created}")
        print("-->".join(str(node_id) for node_id in goal.path()))
    return 0


if __name__ == "__main__":
    sys.exit(main())