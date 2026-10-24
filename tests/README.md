# Search test inputs

**15 cases, each with one origin: 01–08 have multiple goals; 09–15 have one goal.** The original sample (01) and the user's numbering are preserved.

## What distinguishes the methods

A same-cost result is not automatically a weak test. Compare the selected goal, full route, number of moves, total edge cost, and created-node count separately. The suite combines comparison cases with correctness controls.

The current BFS, CUS1 (IDDFS), and CUS2 (move-based IDA*) share the minimum-move objective and ascending-ID route order. They return the same route and cost on this suite; their created-node counts can differ. AS minimizes edge cost on these inputs, while DFS and GBFS need not minimize either cost or moves.

**Cost-separating cases increased from 7/15 to 10/15** by changing only cases 03, 08, and 15. This is one coverage metric, not a proof of overall test accuracy or algorithm correctness.

| Case | Targeted change | Observed cost groups |
| --- | --- | --- |
| 03 | Raise `(4,6)` to 10; add `(3,7): 20` | DFS 13; BFS/GBFS/CUS1/CUS2 22; AS 5 |
| 08 | Add `(2,9): 10` | DFS/BFS/CUS1/CUS2 11; GBFS/AS 3 |
| 15 | Add `(2,8): 20` | DFS/BFS/CUS1/CUS2 23; GBFS/AS 4 |

The other five cases deliberately do not separate returned costs: 02 checks failure/termination; 06 checks equal-priority selection; 07 checks an origin that is already a goal; 10 checks a unique route; 11 checks exploration of branching dead ends. Keep these controls.

## Actual returned costs

| File | Goals | DFS | BFS | GBFS | AS | CUS1 | CUS2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `test01-sample.txt` | 2 | 15 | 10 | 10 | 10 | 10 | 10 |
| `test02-no-path.txt` | 2 | None | None | None | None | None | None |
| `test03-cycle.txt` | 2 | 13 | 22 | 22 | 5 | 22 | 22 |
| `test04-depth-vs-cost.txt` | 2 | 4 | 20 | 20 | 4 | 20 | 20 |
| `test05-cycle-dead-end.txt` | 2 | 5 | 6 | 6 | 5 | 6 | 6 |
| `test06-multiple-goals.txt` | 3 | 2 | 2 | 2 | 2 | 2 | 2 |
| `test07-origin-is-goal.txt` | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| `test08-one-way-unreachable-goal.txt` | 3 | 11 | 11 | 3 | 3 | 11 | 11 |
| `test09-cost-vs-moves.txt` | 1 | 20 | 20 | 3 | 3 | 20 | 20 |
| `test10-simple-line.txt` | 1 | 15 | 15 | 15 | 15 | 15 | 15 |
| `test11-branching-tree.txt` | 1 | 8 | 8 | 8 | 8 | 8 | 8 |
| `test12-one-way-shortcut.txt` | 1 | 6 | 10 | 10 | 5 | 10 | 10 |
| `test13-heuristic_trap.txt` | 1 | 55 | 55 | 55 | 9 | 55 | 55 |
| `test14-expensive_detour.txt` | 1 | 6 | 30 | 30 | 6 | 30 | 30 |
| `test15-branching_dead_ends.txt` | 1 | 23 | 23 | 4 | 4 | 23 | 23 |

`None` means no route exists, rather than a zero-cost solution.

## Independent graph baselines

Minimum moves and minimum cost were independently calculated by exhaustive simple-path enumeration. They are separate objectives and can belong to different routes or goals. Reachable goals describes directed graph reachability; the search methods themselves stop at the first goal.

| File | Origin | Goals | Reachable goals | Minimum moves | Minimum cost |
| --- | ---: | --- | --- | ---: | ---: |
| `test01-sample.txt` | 2 | 5, 4 | 4, 5 | 2 | 10 |
| `test02-no-path.txt` | 1 | 7, 6 | None | None | None |
| `test03-cycle.txt` | 1 | 7, 6 | 6, 7 | 3 | 5 |
| `test04-depth-vs-cost.txt` | 1 | 7, 6 | 6, 7 | 2 | 4 |
| `test05-cycle-dead-end.txt` | 1 | 9, 8 | 8, 9 | 4 | 5 |
| `test06-multiple-goals.txt` | 10 | 40, 30, 20 | 20, 30, 40 | 1 | 2 |
| `test07-origin-is-goal.txt` | 4 | 6, 4, 1 | 1, 4, 6 | 0 | 0 |
| `test08-one-way-unreachable-goal.txt` | 1 | 8, 7, 9 | 9 | 2 | 3 |
| `test09-cost-vs-moves.txt` | 1 | 5 | 5 | 2 | 3 |
| `test10-simple-line.txt` | 10 | 60 | 60 | 5 | 15 |
| `test11-branching-tree.txt` | 1 | 9 | 9 | 4 | 8 |
| `test12-one-way-shortcut.txt` | 6 | 5 | 5 | 2 | 5 |
| `test13-heuristic_trap.txt` | 1 | 4 | 4 | 2 | 9 |
| `test14-expensive_detour.txt` | 1 | 6 | 6 | 1 | 6 |
| `test15-branching_dead_ends.txt` | 9 | 8 | 8 | 3 | 4 |

## Coverage by case

- `test01-sample.txt`: Original assignment sample; preserved byte for byte.
- `test02-no-path.txt`: No-path control: neither goal is reachable; the origin component contains a cycle.
- `test03-cycle.txt`: Cycles with three route choices: DFS takes a deep route costing 13; minimum-move methods take an expensive shortcut costing 22; AS reaches another route costing 5.
- `test04-depth-vs-cost.txt`: Two goals: a two-move route costs 20, while a four-move route costs 4.
- `test05-cycle-dead-end.txt`: A cyclic dead end and two reachable goals; minimum moves and minimum cost select different goals.
- `test06-multiple-goals.txt`: Tie control: shuffled input, nonconsecutive IDs, and three equal-cost goals; the expected selected goal is 20.
- `test07-origin-is-goal.txt`: Zero-step control: origin 4 is one of three goals; expect path [4], cost 0, moves 0, and one created node.
- `test08-one-way-unreachable-goal.txt`: Only goal 9 is reachable; goals 7 and 8 have links in the wrong direction. A two-move shortcut costs 11; the three-move route costs 3.
- `test09-cost-vs-moves.txt`: One goal: the two-move route costs 20 and the three-move route costs 3.
- `test10-simple-line.txt`: Unique-route control: a five-edge directed line with unequal weights; expect the same route and cost from every method.
- `test11-branching-tree.txt`: Branching-tree control: one solution path and several dead leaves; compare created nodes even when all solution costs match.
- `test12-one-way-shortcut.txt`: Converging directed branches and a shortcut: DFS, minimum-move methods, and AS produce three different costs.
- `test13-heuristic_trap.txt`: Greedy trap: the geometrically tempting route costs 55, while the longer alternative costs 9.
- `test14-expensive_detour.txt`: A direct edge costs 30; a five-move detour costs 6.
- `test15-branching_dead_ends.txt`: A self-loop, cycles, and a dead branch. A new three-move exit from the cycle costs 23; the four-move alternative costs 4.

## Run all six methods

From the project root:

```sh
for input in tests/*.txt; do
  for method in DFS BFS GBFS AS CUS1 CUS2; do
    python3 -B search.py "$input" "$method"
  done
done
```

Validation: **90/90 actual CLI runs passed**, using Python 3.14.5. Checks covered valid directed routes, reachable/unreachable outcomes, minimum moves for BFS/CUS1/CUS2, minimum cost for AS, and the explicit tie and zero-step controls.

Every edge has a positive integer cost at least its Euclidean length, making the current AS Euclidean heuristic admissible and consistent on these fixtures. Created-node counts are implementation observations, including repeated rounds; they are not measured runtime, peak memory, or independently proven counts. Full assignment compliance and large-graph performance were not audited.
