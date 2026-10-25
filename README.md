# COS30019 Assignment 2A: Tree-Based Search

Group 2, Introduction to Artificial Intelligence (COS30019), Swinburne University of Technology.

This project solves the **Route Finding** problem with tree-based search. A program reads a map (nodes joined by one-way roads with costs), starts at an origin node, and searches for a destination node with the selected method.

- **Standard task:** stop as soon as any one destination is reached. Six methods are implemented: DFS, BFS, GBFS, AS (A*), CUS1 (IDDFS) and CUS2 (IDA*).
- **Research extension:** the robot must visit **all** destinations at the lowest total cost. All six methods have a modified version (see [Research extension](#research-extension-visit-all-destinations)).

## Requirements

- Python 3 (tested with Python 3.12)
- No third-party libraries (standard library only)
- Tested on Windows (Command Prompt); also runs on macOS and Linux

## Quick start

From the folder that contains the program files:

```text
python search.py <filename> <method>
```

Example (DFS on the sample problem):

```text
python search.py tests\test01-sample.txt DFS
```

On macOS or Linux use `/` in the path (`tests/test01-sample.txt`). On Windows you can also use the batch wrapper: `search <filename> <method>`.

`<method>` is one of `DFS`, `BFS`, `GBFS`, `AS`, `CUS1` or `CUS2` (case-insensitive).

## Search methods

| Method | Algorithm | Type | Notes |
| ------ | --------- | ---- | ----- |
| `DFS` | Depth-First Search | Uninformed | Stack. Follows one path as deep as possible, then backtracks. |
| `BFS` | Breadth-First Search | Uninformed | Queue. Expands level by level, so it finds the path with the fewest moves. |
| `GBFS` | Greedy Best-First Search | Informed | Expands the node with the smallest `h(n)`. Fast, but can choose an expensive path. |
| `AS` | A* Search | Informed | Expands the node with the smallest `f(n) = g(n) + h(n)`, where `g(n)` is the path cost so far. |
| `CUS1` | Iterative Deepening DFS (IDDFS) | Uninformed (custom) | Repeats depth-limited DFS with limit 0, 1, 2, ... Finds the path with the fewest moves. |
| `CUS2` | Iterative Deepening A* (IDA*) | Informed (custom) | Repeats DFS with a limit on `f(n) = g(n) + h(n)`, then raises the limit to the smallest `f` that was exceeded. Here `g(n)` counts **moves** and `h(n)` estimates the moves still needed. Finds the path with the fewest moves. |

### Heuristic

- **GBFS and AS:** straight-line (Euclidean) distance from a node to the nearest destination.
- **CUS2 (IDA\*):** distance to the nearest destination divided by the longest straight-line edge length, rounded up. This never overestimates the number of moves remaining.

### Tree-based search and cycles

These are tree-based searches, so no explored set is kept. To avoid endless loops, a node is never expanded to a child that already appears on its own path from the origin.

### Tie-breaking

When all else is equal, children are expanded in ascending node-ID order. When two nodes on different branches are equal, the one added first is expanded first. The input loader sorts destinations and outgoing edges by node ID so results are deterministic.

## Input file format

A problem file has four parts:

```text
Nodes:
1: (4,1)
2: (2,2)
3: (4,4)
Edges:
(2,1): 4
(3,1): 5
(2,3): 4

Origin:
2
Destinations:
3; 1
```

- `Nodes:` one node per line, `<id>: (<x>,<y>)`.
- `Edges:` one directed edge per line, `(<from>,<to>): <cost>`. Edges are **one-way**: `(2,1): 4` allows 2 to 1 but not 1 to 2.
- `Origin:` the start node.
- `Destinations:` one or more goal nodes separated by semicolons. The search stops when it reaches any one of them.

The program prints a clear error message (and exits with a non-zero status) if the file cannot be read, an edge uses a node that does not exist, the `Origin` or `Destinations` section is missing, or the method or arguments are invalid.

## Output format

The program prints three lines:

```text
<filename> <method>
<goal-node-or-None> <nodes-created>
<path from origin to goal>
```

- Line 1: the file name and the method.
- Line 2: the goal node reached (or `None`) and the number of nodes created during the search.
- Line 3: the path. If no goal can be reached, this line is empty.

`nodes-created` counts every search-tree node created, including the origin. If the origin is already a destination, the search stops at once with 1 node and a path of just the origin. For `CUS1` and `CUS2` the count adds up over all rounds, because each round rebuilds the tree from the origin.

### Example runs

Using `tests\test01-sample.txt` (origin 2, destinations 5 and 4):

```text
> python search.py tests\test01-sample.txt BFS
tests\test01-sample.txt BFS
4 10
2 1 4
```

| Method | Goal | Nodes | Path | Cost |
| ------ | ---: | ----: | ---- | ---: |
| DFS | 5 | 7 | 2 1 3 5 | 15 |
| BFS | 4 | 10 | 2 1 4 | 10 |
| GBFS | 5 | 6 | 2 3 5 | 10 |
| AS | 4 | 8 | 2 1 4 | 10 |
| CUS1 | 4 | 9 | 2 1 4 | 10 |
| CUS2 | 4 | 4 | 2 1 4 | 10 |

When no destination can be reached (`tests\test02-no-path.txt`):

```text
> python search.py tests\test02-no-path.txt BFS
tests\test02-no-path.txt BFS
None 4

```

## Research extension: visit all destinations

The standard task stops at the first destination. In the research version, a route is complete only when **every** destination has been visited, and the search looks for the lowest total cost.

### How to run

```text
python search_all.py <filename> <method>
```

Example (BFS, visit-all, on test01):

```text
python search_all.py tests\test01-sample.txt BFS
```

Input files and method names are the same as in the standard version, and the output has the same three lines, with two differences:

- The goal on line 2 is the **last node of the route**, and the route may pass through the same node more than once.
- `None` means that no route can visit every destination (line 3 is empty).

Example (A* on test01): the standard search reaches one destination at cost 10 (`2 1 4`), while visiting both destinations costs 17:

```text
> python search_all.py tests\test01-sample.txt AS
tests\test01-sample.txt AS
5 16
2 1 4 5
```

### What was modified

| Challenge | Solution |
| --------- | -------- |
| Stopping at the first destination is no longer enough | The goal test requires that every destination has been visited |
| A route may pass through the same node more than once | The search state is (current node, set of visited destinations), not the node alone |
| Searching for better routes could continue without end | Branch and bound: keep the best complete cost found so far and prune routes that cannot beat it |
| The origin may itself be a destination | The origin is added to the visited set at the start |
| A* and IDA* need an estimate of the remaining cost | `h` = distance from the current node to the farthest unvisited destination |

The research version was tested on `test01` to `test08` (the cases with more than one destination). Results and discussion are in the report (Research section and Appendix B).

## Test files

The 15 problem files are in `tests/`, grouped by goal count: **01-08 have more than one destination; 09-15 have a single destination.** See [the test guide](tests/README.md) for expected results.

| File | Goals | What it checks |
| --- | ---: | --- |
| `test01-sample.txt` | 2 | Original assignment sample. |
| `test02-no-path.txt` | 2 | No path: neither goal is reachable; the origin's part of the graph contains a cycle. |
| `test03-cycle.txt` | 2 | Cycles with three route choices: a deep route (cost 13), an expensive shortcut (cost 22) and a cheap route (cost 5). |
| `test04-depth-vs-cost.txt` | 2 | A two-move route costs 20; a four-move route costs 4. |
| `test05-cycle-dead-end.txt` | 2 | A cyclic dead end and two reachable goals; fewest moves and lowest cost pick different goals. |
| `test06-multiple-goals.txt` | 3 | Tie-break check: shuffled input, non-consecutive IDs and three equal-cost goals (expected goal 20). |
| `test07-origin-is-goal.txt` | 3 | The origin (node 4) is one of the goals: path is just node 4, cost 0, 1 node created. |
| `test08-one-way-unreachable-goal.txt` | 3 | Only goal 9 is reachable; the other goals have links in the wrong direction. A two-move shortcut costs 11; the three-move route costs 3. |
| `test09-cost-vs-moves.txt` | 1 | A two-move route costs 20; a three-move route costs 3. |
| `test10-simple-line.txt` | 1 | A directed line: every method should return the same route and cost. |
| `test11-branching-tree.txt` | 1 | One solution path and several dead ends; compares nodes created when all costs match. |
| `test12-one-way-shortcut.txt` | 1 | Converging directed branches and a shortcut: DFS, fewest-moves methods and A* give three different costs. |
| `test13-heuristic_trap.txt` | 1 | Greedy trap: the route that looks closest costs 55; the longer route costs 9. |
| `test14-expensive_detour.txt` | 1 | A direct edge costs 30; a five-move detour costs 6. |
| `test15-branching_dead_ends.txt` | 1 | A self-loop, cycles and a dead branch: an exit costs 23, the longer alternative costs 4. |

## Files

**Standard search**

- `search.py` - Command-line entry point and method selection.
- `problem.py` - Problem representation and file loading.
- `node.py` - Search-tree node.
- `heuristic.py` - Heuristic (distance to the nearest destination).
- `dfs.py`, `bfs.py`, `gbfs.py`, `astar.py` - DFS, BFS, GBFS and A*.
- `iddfs.py` - CUS1: Iterative Deepening DFS.
- `ida_star.py` - CUS2: Iterative Deepening A* (counts moves).

**Research extension (visit all destinations)**

- `search_all.py` - Command-line entry point for the research version.
- `all_common.py` - Shared logic used by all six modified methods.
- `all_dfs.py`, `all_bfs.py`, `all_gbfs.py`, `all_astar.py` - Modified DFS, BFS, GBFS and A*.
- `all_iddfs.py`, `all_ida_star.py` - Modified CUS1 and CUS2.

**Other**

- `tests/` - The 15 test problem files.