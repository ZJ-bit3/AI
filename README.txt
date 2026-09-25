================================================================================
                      CS188 Pacman Search Project
                     AI2002 - Artificial Intelligence
                  FAST-NUCES | Fall 2026 | i243130
================================================================================

STUDENT INFO
============
Name:           Zain Jabir
Roll Number:    i243130
Section:        [Your Section]
Instructor:     [Instructor Name]

SYSTEM SPECS
============
OS:             Ubuntu 22.04 LTS (Linux)
Python:         3.12.3
Processor:      [Your Processor, e.g., Intel Core i7-12700H]
RAM:            [Your RAM, e.g., 16 GB]

HOW TO RUN
==========

All commands should be run from the search/ directory.

--- Task 1: Depth-First Search ---
python3 pacman.py -l tinyMaze -p SearchAgent
python3 pacman.py -l mediumMaze -p SearchAgent
python3 pacman.py -l bigMaze -p SearchAgent -z .5

--- Task 2: Breadth-First Search ---
python3 pacman.py -l tinyMaze -p SearchAgent -a fn=bfs
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python3 pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5

--- Task 3: Uniform-Cost Search ---
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python3 pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python3 pacman.py -l mediumScaryMaze -p StayWestSearchAgent

--- Task 4: Greedy Best-First Search ---
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
python3 pacman.py -l bigMaze -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic -z .5

--- Task 5: A* Search ---
python3 pacman.py -l bigMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic -z .5

--- Task 6: CSV Trace Evidence ---
Evidence CSVs are auto-generated in evidence/ when any search runs.
Example: evidence/dfs_tinyMaze.csv, evidence/astar_bigMaze.csv

--- Task 7: Corners Problem ---
python3 pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python3 pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem

--- Task 8: Corners Heuristic ---
python3 pacman.py -l mediumCorners -p AStarCornersAgent -z .5

--- Task 9: Food Heuristic ---
python3 pacman.py -l trickySearch -p AStarFoodSearchAgent

--- Task 10: Closest Dot (AnyFoodSearchProblem) ---
python3 pacman.py -l bigSearch -p ClosestDotSearchAgent

--- Custom Maze: i243130Search ---
python3 pacman.py -l i243130Search -p SearchAgent -a fn=dfs
python3 pacman.py -l i243130Search -p SearchAgent -a fn=bfs
python3 pacman.py -l i243130Search -p SearchAgent -a fn=ucs
python3 pacman.py -l i243130Search -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
python3 pacman.py -l i243130Search -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

--- Run Autograder ---
python3 autograder.py

NOTES
=====
- Only search.py and searchAgents.py were modified.
- CSV trace logs are written to evidence/<algorithm>_<layout>.csv
- The custom maze i243130Search.lay is in layouts/
- Add -q flag for quiet (no graphics) mode, -t for text display.
