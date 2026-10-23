# Search test inputs

There are **15 graph inputs: 8 with multiple goals and 7 with one goal**. Every case has exactly one origin. `test01-sample.txt` is unchanged.

Multiple-goal files: **01, 02, 03, 04, 05, 06, 10, 11**. Single-goal files: **07, 08, 09, 12, 13, 14, 15**.

The balanced split improves goal-count coverage; the different graph scenarios also test reachability, direction, cycles, ties, dead ends, and moves versus cost.

## Independent baselines

These baselines come from exhaustive enumeration of simple directed paths, independently of the six project algorithms. Minimum moves and minimum cost are separate objectives and can belong to different routes or goals. `None` means that no destination is reachable.

| File | Origin | Goals | Reachable goals | Minimum moves | Minimum cost |
| --- | ---: | --- | --- | ---: | ---: |
| `test01-sample.txt` | 2 | 5, 4 | 4, 5 | 2 | 10 |
| `test02-no-path.txt` | 1 | 7, 6 | None | None | None |
| `test03-cycle.txt` | 1 | 7, 6 | 6, 7 | 4 | 4 |
| `test04-depth-vs-cost.txt` | 1 | 7, 6 | 6, 7 | 2 | 4 |
| `test05-cycle-dead-end.txt` | 1 | 9, 8 | 8, 9 | 4 | 5 |
| `test06-multiple-goals.txt` | 10 | 40, 30, 20 | 20, 30, 40 | 1 | 2 |
| `test07-simple-line.txt` | 10 | 60 | 60 | 5 | 15 |
| `test08-branching-tree.txt` | 1 | 9 | 9 | 4 | 8 |
| `test09-cost-vs-moves.txt` | 1 | 5 | 5 | 2 | 3 |
| `test10-origin-is-goal.txt` | 4 | 6, 4, 1 | 1, 4, 6 | 0 | 0 |
| `test11-one-way-unreachable-goal.txt` | 1 | 8, 7, 9 | 9 | 3 | 3 |
| `test12-one-way-shortcut.txt` | 6 | 5 | 5 | 2 | 5 |
| `test13-heuristic_trap.txt` | 1 | 4 | 4 | 2 | 9 |
| `test14-expensive_detour.txt` | 1 | 6 | 6 | 1 | 6 |
| `test15-branching_dead_ends.txt` | 9 | 8 | 8 | 4 | 4 |

## Purpose of each case

- `test01-sample.txt`: Original assignment sample; preserved byte for byte.
- `test02-no-path.txt`: Both goals are in a disconnected component; the reachable component contains a cycle.
- `test03-cycle.txt`: Two reachable goals, several directed cycles, and a dead end; both best routes need four moves.
- `test04-depth-vs-cost.txt`: Goal 7 takes two moves costing 20; goal 6 takes four moves costing 4.
- `test05-cycle-dead-end.txt`: A low-ID branch is a cyclic dead end; the other branch offers a short expensive goal and a longer cheap goal.
- `test06-multiple-goals.txt`: Three equal-cost, equally near goals; shuffled input and nonconsecutive IDs exercise ascending-ID ties.
- `test07-simple-line.txt`: One directed route with five moves and unequal weights; all methods should return the same path.
- `test08-branching-tree.txt`: An acyclic branching tree with several dead leaves and one goal; includes negative coordinates.
- `test09-cost-vs-moves.txt`: The same goal has a two-move route costing 20 and a three-move route costing 3.
- `test10-origin-is-goal.txt`: The non-1 origin is one of three goals: every method should return [4], zero moves and one created node.
- `test11-one-way-unreachable-goal.txt`: Goals 7 and 8 only have outgoing links toward the origin component; only goal 9 is reachable.
- `test12-one-way-shortcut.txt`: Converging branches reach node 3 at different costs; a one-way shortcut uses fewer moves but costs more.
- `test13-heuristic_trap.txt`: Greedy follows the geometrically close node 2 and pays 55; the four-move alternative costs 9.
- `test14-expensive_detour.txt`: An expensive direct edge costs 30; the five-move detour costs 6.
- `test15-branching_dead_ends.txt`: Two branches cannot reach the goal, including a self-loop and a cycle to the origin; the third reaches goal 8.

## Running the cases

From the project root, run all 90 case/method combinations:

```sh
for input in tests/*.txt; do
  for method in DFS BFS GBFS AS CUS1 CUS2; do
    python3 -B search.py "$input" "$method"
  done
done
```

Check that every returned route follows the directed edges and ends at a listed goal. BFS, CUS1 (IDDFS), and CUS2 (the current move-based IDA*) should match minimum moves. AS should match minimum cost; DFS and GBFS need not optimize either objective.

All edges have positive integer costs at least as large as their Euclidean lengths, so the current AS Euclidean heuristic is admissible and consistent on these inputs. Case 06 expects goal 20 for equal priorities despite shuffled input. Case 10 expects the origin alone, zero moves, zero cost, and one created node.

The suite was validated with all six methods (90 runs). General created-node counts are recorded as observations, rather than asserted as independently proven counts. This is fixture validation, not a full audit of the assignment implementation.
