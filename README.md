# COS30019 Assignment 2A: Tree-Based Search

This project implements tree-based search methods for a route-finding problem. It reads a graph description from an input file, starts at the specified origin node, and searches for one of the destination nodes using the selected method.

All six required search methods are implemented: DFS, BFS, GBFS, AS, CUS1 and CUS2.

## Requirements

- Python 3 (tested with Python 3.12)
- No third-party libraries are required.

## Running the program

On macOS or Linux, run:

```text
python search.py <filename> <method>
```

On Windows, run:

```text
search <filename> <method>
```

For example:

```text
python search.py tests/test01-sample.txt DFS
```

The method name is case-insensitive (`dfs`, `Dfs` and `DFS` are all accepted).

## Search methods

| Method | Algorithm | Type | Notes |
| ------ | --------- | ---- | ----- |
| `DFS` | Depth-First Search | Uninformed | Uses a stack. Children are expanded in ascending node-ID order. |
| `BFS` | Breadth-First Search | Uninformed | Uses a queue and expands level by level. |
| `GBFS` | Greedy Best-First Search | Informed | Expands the node with the smallest heuristic value `h(n)` only. Not guaranteed to be optimal. |
| `AS` | A* Search | Informed | Expands the node with the smallest `f(n) = g(n) + h(n)` using a priority queue. |
| `CUS1` | Iterative Deepening DFS (IDDFS) | Uninformed (custom) | Repeats depth-limited DFS with an increasing depth limit. |
| `CUS2` | Iterative Deepening A* (IDA*) | Informed (custom) | Repeats cost-limited DFS, raising the `f`-cost threshold each round. |

### Heuristic

The informed methods (GBFS, AS, CUS2) use the straight-line (Euclidean) distance from a node to the **nearest destination**. IDA* scales this value by the smallest ratio of edge cost to edge length so that it never overestimates the remaining cost.

### Tree-based search and cycles

These are tree-based searches, so no explored-set is kept. To avoid infinite loops, a node is never expanded to a child that already appears on its own path from the origin.

### Tie-breaking

To keep results deterministic, children are always considered in ascending node-ID order. The input loader also sorts destinations and outgoing edges by node ID.

## Input file format

An input file contains four sections:

- `Nodes`: each node is written as `<id>: (<x>,<y>)`.
- `Edges`: each directed edge is written as `(<from>,<to>): <cost>`.
- `Origin`: the ID of the starting node.
- `Destinations`: one or more destination IDs separated by semicolons.

Example:

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

The program reports an error message (and exits with a non-zero status) if the file cannot be read, an edge refers to an unknown node, or the `Origin` / `Destinations` section is missing or refers to an unknown node.

## Output format

The program produces three lines:

```text
<filename> <method>
<destination-node-id-or-None> <nodes-created>
<node-id-1> <node-id-2> ... <node-id-n>
```

- Line 1: the input filename and the method used.
- Line 2: the destination node that was reached (or `None`) and the number of nodes created during the search.
- Line 3: the path from the origin to that destination. If no path is found, this line is blank.

`nodes-created` counts every search-tree node that was created, including the origin. For `CUS1` (IDDFS) the count is accumulated over all iterations, because each iteration rebuilds the tree from the origin.

### Example runs

Using `tests/test01-sample.txt` (origin `2`, destinations `5` and `4`):

```text
$ python search.py tests/test01-sample.txt DFS
tests/test01-sample.txt DFS
5 7
2 1 3 5

$ python search.py tests/test01-sample.txt BFS
tests/test01-sample.txt BFS
4 10
2 1 4

$ python search.py tests/test01-sample.txt GBFS
tests/test01-sample.txt GBFS
5 6
2 3 5

$ python search.py tests/test01-sample.txt AS
tests/test01-sample.txt AS
4 8
2 1 4

$ python search.py tests/test01-sample.txt CUS1
tests/test01-sample.txt CUS1
4 9
2 1 4

$ python search.py tests/test01-sample.txt CUS2
tests/test01-sample.txt CUS2
4 18
2 1 4
```

When no path exists (`tests/test02-no-path.txt`):

```text
$ python search.py tests/test02-no-path.txt DFS
tests/test02-no-path.txt DFS
None 2

```

## Test files

The `tests/` folder contains input files covering common situations:

| File | What it checks |
| ---- | -------------- |
| `test01-sample.txt` | The sample problem from the assignment |
| `test02-no-path.txt` | No route to any destination |
| `test03-cycle.txt` | A cycle in the graph |
| `test04-depth-vs-cost.txt` | Shallow path vs. cheap path |
| `test05-cycle-dead-end.txt` | A cycle combined with a dead end |
| `test06-multiple-goals.txt` | More than one destination |
| `test07-simple-line.txt` | A simple straight line of nodes |
| `test08-branching-tree.txt` | A branching tree |
| `test09-cost-vs-moves.txt` | Fewest moves vs. lowest cost |
| `test10-origin-is-goal.txt` | The origin is already a destination |
| `test11-one-way-unreachable-goal.txt` | One-way edges make a goal unreachable |
| `test12-one-way-shortcut.txt` | A one-way shortcut |
| `test13-heuristic_trap.txt` | A heuristic that misleads greedy search |
| `test14-expensive_detour.txt` | An expensive detour |
| `test15-branching_dead_ends.txt` | Branching with many dead ends |

To run every method on one test file (macOS / Linux):

```text
for m in DFS BFS GBFS AS CUS1 CUS2; do python search.py tests/test01-sample.txt $m; done
```

## Files

- `search.py` - Command-line entry point and search-method selection.
- `problem.py` - Input problem representation and file loading.
- `node.py` - Search-tree node representation.
- `heuristic.py` - Heuristic-related code (distance to the nearest destination).
- `dfs.py` - Depth-First Search implementation.
- `bfs.py` - Breadth-First Search implementation.
- `gbfs.py` - Greedy Best-First Search implementation.
- `astar.py` - A* Search implementation.
- `iddfs.py` - Custom Search 1: Iterative Deepening DFS.
- `ida_star.py` - Custom Search 2: Iterative Deepening A*.
- `search.bat` - Windows command wrapper for `search.py`.
- `tests/` - Sample and edge-case input files.
- `Assignment2/` - Assignment specification, team contribution record and meeting record.