# COS30019 Assignment 2A: Tree-Based Search

This project implements tree-based search methods for the Route Finding problem. It reads a graph description from an input file, starts at the specified origin node, and searches for a destination node using the selected method.

All six required search methods are implemented: DFS, BFS, GBFS, AS, CUS1 and CUS2.

The project also includes a research extension (`search_all.py`) that modifies the methods so the route must **visit all destination nodes** at the lowest total cost. See [Research extension: visit all destinations](#research-extension-visit-all-destinations).

## Requirements

- Python 3 (tested with Python 3.12)
- No third-party libraries are required.

## Running the program

On Windows (Command Prompt), run:

```text
python search.py <filename> <method>
```

On macOS or Linux, run:

```text
python search.py <filename> <method>
```

For example:

```text
python search.py tests/test01-sample.txt DFS
```

`<method>` is one of `DFS`, `BFS`, `GBFS`, `AS`, `CUS1` or `CUS2`. The method name is case-insensitive (`dfs`, `Dfs` and `DFS` are all accepted).

## Search methods

| Method | Algorithm | Type | Notes |
| ------ | --------- | ---- | ----- |
| `DFS` | Depth-First Search | Uninformed | Uses a stack. Children are expanded in ascending node-ID order. |
| `BFS` | Breadth-First Search | Uninformed | Uses a queue and expands level by level. Finds the path with the fewest moves. |
| `GBFS` | Greedy Best-First Search | Informed | Expands the node with the smallest heuristic value `h(n)` only. Not guaranteed to be optimal. |
| `AS` | A* Search | Informed | Expands the node with the smallest `f(n) = g(n) + h(n)` using a priority queue, where `g(n)` is the path cost so far. |
| `CUS1` | Iterative Deepening DFS (IDDFS) | Uninformed (custom) | Repeats depth-limited DFS with an increasing depth limit. Finds the path with the fewest moves. |
| `CUS2` | Iterative Deepening A* (IDA*) | Informed (custom) | Repeats DFS with a limit on `f(n) = g(n) + h(n)`, raising the limit each round. Here `g(n)` is the number of moves and `h(n)` is an admissible estimate of the moves still needed. Finds the path with the fewest moves. |

### Heuristic

- **GBFS and AS** use the straight-line (Euclidean) distance from a node to the **nearest destination**.
- **CUS2 (IDA\*)** counts moves, not cost. Its `h(n)` is the distance to the nearest destination divided by the longest edge in the graph, rounded up, so it never overestimates the number of moves remaining.

### Tree-based search and cycles

These are tree-based searches, so no explored-set is kept. To avoid infinite loops, a node is never expanded to a child that already appears on its own path from the origin.

### Tie-breaking

To keep results deterministic, children are always considered in ascending node-ID order. When all else is equal, nodes on different branches are expanded in the order they were added. The input loader also sorts destinations and outgoing edges by node ID.

## Input file format

An input file contains four sections:

- `Nodes`: each node is written as `<id>: (<x>,<y>)`.
- `Edges`: each directed edge is written as `(<from>,<to>): <cost>`. Edges are one-way.
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

The program reports an error message (and exits with a non-zero status) if the file cannot be read, an edge refers to an unknown node, or the `Origin` / `Destinations` section is missing or refers to an unknown node. A missing file, an unknown method and a missing argument also give a clear message without crashing.

## Output format

The program produces three lines:

```text
<filename> <method>
<destination-node-id-or-None> <nodes-created>
<node-id-1>--><node-id-2>-->...--><node-id-n>
```

- Line 1: the input filename and the method used.
- Line 2: the destination node that was reached (or `None`) and the number of nodes created during the search.
- Line 3: the path from the origin to that destination. If no path is found, this line is blank.

`nodes-created` counts every search-tree node that was created, including the origin. If the origin is already a destination, the search stops at once with 1 node created and a path of just the origin. For `CUS1` (IDDFS) and `CUS2` (IDA*), the count is accumulated over all rounds, because each round rebuilds the tree from the origin, so the origin is counted again in every round.

### Example runs

Using `tests/test01-sample.txt` (origin `2`, destinations `5` and `4`):

```text
$ python search.py tests/test01-sample.txt DFS
tests/test01-sample.txt DFS
5 7
2-->1-->3-->5

$ python search.py tests/test01-sample.txt BFS
tests/test01-sample.txt BFS
4 10
2-->1-->4

$ python search.py tests/test01-sample.txt GBFS
tests/test01-sample.txt GBFS
5 6
2-->3-->5

$ python search.py tests/test01-sample.txt AS
tests/test01-sample.txt AS
4 8
2-->1-->4

$ python search.py tests/test01-sample.txt CUS1
tests/test01-sample.txt CUS1
4 9
2-->1-->4

$ python search.py tests/test01-sample.txt CUS2
tests/test01-sample.txt CUS2
4 4
2-->1-->4
```

When no path exists (`tests/test02-no-path.txt`):

```text
$ python search.py tests/test02-no-path.txt DFS
tests/test02-no-path.txt DFS
None 4

```

## Research extension: visit all destinations

The standard task stops as soon as one destination is reached. The research extension changes the goal: the route must **visit every destination** with the lowest total path cost.

### How to run

```text
python search_all.py <filename> <method>
```

For example:

```text
python search_all.py tests/test01-sample.txt AS
```

The input file format and method names are the same as for the standard program. The output has the same three lines, with these differences:

- The goal on line 2 is the **last node of the route**.
- The route may pass through the same node more than once.
- If no route can visit every destination, line 2 shows `None` and line 3 is blank.

### What was modified

- **State:** a search state is the current node together with the set of destinations already visited, not the node alone. Loop avoidance checks this state, so a node can be revisited when the visited set is different.
- **Goal test:** a branch is complete only when all destinations have been visited. The origin counts as visited at the start if it is a destination.
- **Branch and bound (DFS, BFS, GBFS, CUS1):** the search keeps the best complete cost found so far and prunes any route that cannot beat it, instead of stopping at the first complete route.
- **A\* and IDA\* (AS, CUS2):** use `f(n) = g(n) + h(n)` with the accumulated cost and a heuristic estimate of the remaining cost (distance to the farthest unvisited destination).

The research tests use `test01` to `test08`, which have more than one destination. Results and discussion are in the report (Research section and Appendix B).

## Test files

The 15 inputs are grouped by goal count: **01-08 multiple goals; 09-15 a single goal**. See [the test guide](tests/README.md) for expected results, comparison cases, and correctness controls.

| File | Goals | What it checks |
| --- | ---: | --- |
| `test01-sample.txt` | 2 | Original assignment sample; preserved byte for byte. |
| `test02-no-path.txt` | 2 | No-path control: neither goal is reachable; the origin component contains a cycle. |
| `test03-cycle.txt` | 2 | Cycles with three route choices: DFS takes a deep route costing 13; minimum-move methods take an expensive shortcut costing 22; AS reaches another route costing 5. |
| `test04-depth-vs-cost.txt` | 2 | Two goals: a two-move route costs 20, while a four-move route costs 4. |
| `test05-cycle-dead-end.txt` | 2 | A cyclic dead end and two reachable goals; minimum moves and minimum cost select different goals. |
| `test06-multiple-goals.txt` | 3 | Tie control: shuffled input, nonconsecutive IDs, and three equal-cost goals; the expected selected goal is 20. |
| `test07-origin-is-goal.txt` | 3 | Zero-step control: origin 4 is one of three goals; expect path [4], cost 0, moves 0, and one created node. |
| `test08-one-way-unreachable-goal.txt` | 3 | Only goal 9 is reachable; goals 7 and 8 have links in the wrong direction. A two-move shortcut costs 11; the three-move route costs 3. |
| `test09-cost-vs-moves.txt` | 1 | One goal: the two-move route costs 20 and the three-move route costs 3. |
| `test10-simple-line.txt` | 1 | Unique-route control: a five-edge directed line with unequal weights; expect the same route and cost from every method. |
| `test11-branching-tree.txt` | 1 | Branching-tree control: one solution path and several dead leaves; compare created nodes even when all solution costs match. |
| `test12-one-way-shortcut.txt` | 1 | Converging directed branches and a shortcut: DFS, minimum-move methods, and AS produce three different costs. |
| `test13-heuristic_trap.txt` | 1 | Greedy trap: the geometrically tempting route costs 55, while the longer alternative costs 9. |
| `test14-expensive_detour.txt` | 1 | A direct edge costs 30; a five-move detour costs 6. |
| `test15-branching_dead_ends.txt` | 1 | A self-loop, cycles, and a dead branch. A new three-move exit from the cycle costs 23; the four-move alternative costs 4. |

## Files

- `search.py` - Command-line entry point and search-method selection.
- `search_all.py` - Command-line entry point for the research extension (visit all destinations).
- `problem.py` - Input problem representation and file loading.
- `node.py` - Search-tree node representation.
- `heuristic.py` - Heuristic code (distance to the nearest destination).
- `dfs.py` - Depth-First Search implementation.
- `bfs.py` - Breadth-First Search implementation.
- `gbfs.py` - Greedy Best-First Search implementation.
- `astar.py` - A* Search implementation.
- `iddfs.py` - Custom Search 1: Iterative Deepening DFS.
- `ida_star.py` - Custom Search 2: Iterative Deepening A*.
- `tests/` - Sample and edge-case input files.
