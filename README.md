# AI-Programming-Assignment5-se24ucse253

# AI Lab Assignment

Name: Reyansh Chamakura
Roll No: se24ucse253 
Course: Artificial Intelligence

---

## i put all my files in this repo itself

```
├── game.py              # tic tac toe board logic (shared)
├── minimax.py
├── alpha_beta.py
├── heuristic_ab.py
├── mcts.py
├── test_algorithms.py   # run this for part 1 tests
│
├── travel_planner.py    # part 2
├── knowledge_graphs.py  # part 3
├── bayesian_network.py  # part 4
│
└── README.md
```

---


## Part 1 — Search Algorithms

Four algorithms on Tic-Tac-Toe:

- **Minimax** — searches the full game tree, picks the optimal move
- **Alpha-Beta** — same result as minimax but skips branches that won't matter
- **Heuristic Alpha-Beta** — adds a depth limit and eval function so it doesn't go all the way down
- **MCTS** — runs random simulations and picks the move that wins most

`test_algorithms.py` runs four test cases:
1. Win in one move (expects cell 2)
2. Block opponent from winning (expects cell 5)
3. Empty board (any sensible opening move)
4. Near-draw with only one cell left

It also prints how many nodes Minimax vs Alpha-Beta explored on an empty board. Alpha-Beta cuts a lot.

---

## Part 2 — Travel Planner

Uses three knowledge bases (places, food preferences, activities) to score and rank destinations for a given user profile. Then generates a day-by-day plan with estimated cost.

Two test profiles are included — one budget beach trip, one history + culture trip.

---

## Part 3 — Knowledge Graphs

Builds a simple triple store: `(Subject, Predicate, Object)`.

Example triples like `(Paris, locatedIn, France)` and `(EiffelTower, isA, Landmark)` are added, then queried by subject/predicate/object.

The file also includes equivalent RDFLib code (commented) showing how this maps to a real KG library, and a quick table of tools like Neo4j, Protege, Apache Jena.

---

## Part 4 — Bayesian Network

Models student exam performance:

```
Study ──┐
        ├──▶ Grade ──▶ Pass
Diff ───┘
```

CPTs are defined manually. Inference by enumeration — sums over all variable combos. Runs several probability queries and a sanity check (joint distribution should sum to 1.0).

---

