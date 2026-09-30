# COS30019 Assignment 2A: Tree-Based Search

This project implements tree-based search methods for a route-finding problem. It reads a graph description from an input file, starts at the specified origin node, and searches for one of the destination nodes using the selected method. DFS is implemented; BFS, GBFS, AS, CUS1, and CUS2 are not implemented yet.

## Requirements

- Python 3
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
python search.py PathFinder-test-1.txt DFS
```

The method name is case-insensitive. The available methods are:

- `DFS` - Depth-First Search (implemented)
- `BFS` - Breadth-First Search (not implemented yet)
- `GBFS` - Greedy Best-First Search (not implemented yet)
- `AS` - A* Search (not implemented yet)
- `CUS1` - Custom Search 1 (not implemented yet)
- `CUS2` - Custom Search 2 (not implemented yet)

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

## Output format

The program produces three lines:

```text
<filename> <method>
<destination-node-id-or-None> <nodes-created>
<node-id-1> <node-id-2> ... <node-id-n>
```

The third line contains the path from the origin to the selected destination. If no path is found, the second line contains `None` and the third line is blank.

## Files

- `search.py` - Command-line entry point and search-method selection.
- `problem.py` - Input problem representation and file loading.
- `node.py` - Search-tree node representation.
- `dfs.py` - Depth-First Search implementation.
- `heuristic.py` - Heuristic-related code.
- `search.bat` - Windows command wrapper for `search.py`.
