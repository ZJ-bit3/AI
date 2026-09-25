# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import os
import csv


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


# ---------------------------------------------------------------------------
# CSV Trace Logger — shared by all five search functions
# ---------------------------------------------------------------------------

def _get_layout_name():
    """Try to extract the layout name from command-line args."""
    import sys
    args = sys.argv
    for i, arg in enumerate(args):
        if arg in ('-l', '--layout') and i + 1 < len(args):
            return args[i + 1]
    return 'unknown'


def _init_csv(algorithm_name):
    """Create/overwrite the CSV file and return (file_handle, csv_writer)."""
    layout = _get_layout_name()
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'evidence')
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, f'{algorithm_name}_{layout}.csv')
    f = open(filepath, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow([
        'iteration', 'expanded_state', 'parent', 'action',
        'generated_successors', 'frontier_before', 'frontier_after',
        'explored', 'g', 'h', 'f'
    ])
    return f, writer


def _frontier_states(fringe):
    """Extract the list of states currently sitting in any fringe type."""
    if isinstance(fringe, util.Stack) or isinstance(fringe, util.Queue):
        return [node[0] for node in fringe.list]
    elif isinstance(fringe, util.PriorityQueue):
        return [entry[2][0] for entry in fringe.heap]
    return []


def _log_row(writer, iteration, state, parent, action, successors,
             frontier_before, frontier_after, explored, g='', h='', f=''):
    writer.writerow([
        iteration, state, parent, action,
        successors, frontier_before, frontier_after,
        list(explored), g, h, f
    ])


# ---------------------------------------------------------------------------
# 1. Depth-First Search
# ---------------------------------------------------------------------------

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    csv_file, writer = _init_csv('dfs')

    fringe = util.Stack()
    start = problem.getStartState()
    fringe.push((start, []))
    explored = set()
    iteration = 0

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if state in explored:
            continue

        # Goal test BEFORE expanding successors
        iteration += 1
        if problem.isGoalState(state):
            _log_row(writer, iteration, state, '', '', [],
                     _frontier_states(fringe), _frontier_states(fringe), explored)
            csv_file.close()
            return actions

        explored.add(state)
        frontier_before = _frontier_states(fringe)
        successors_raw = problem.getSuccessors(state)

        # Push successors in original order — LIFO means last pushed = first popped
        for successor, action, cost in successors_raw:
            if successor not in explored:
                fringe.push((successor, actions + [action]))

        frontier_after = _frontier_states(fringe)
        generated = [s[0] for s in successors_raw]
        parent = actions[-1] if actions else 'Start'
        _log_row(writer, iteration, state, parent,
                 actions[-1] if actions else 'None', generated,
                 frontier_before, frontier_after, explored)

    csv_file.close()
    return []

"""
HOW DFS WORKS:
DFS uses a stack (LIFO) as its fringe, so it always expands the most recently
added node — diving deep down one branch before backtracking. We maintain an
explored set to avoid revisiting states (graph search). Successors are pushed in
reverse of the desired N->E->S->W order so that North is popped first. The path
is reconstructed by carrying the full action list with each node on the stack.
"""


# ---------------------------------------------------------------------------
# 2. Breadth-First Search
# ---------------------------------------------------------------------------

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    csv_file, writer = _init_csv('bfs')

    fringe = util.Queue()
    start = problem.getStartState()
    fringe.push((start, []))
    explored = set()
    in_fringe = set()
    in_fringe.add(start)
    iteration = 0

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            iteration += 1
            _log_row(writer, iteration, state, '', '', [],
                     _frontier_states(fringe), _frontier_states(fringe), explored)
            csv_file.close()
            return actions

        explored.add(state)
        iteration += 1
        frontier_before = _frontier_states(fringe)

        successors_raw = problem.getSuccessors(state)
        generated = []
        for successor, action, cost in successors_raw:
            if successor not in explored and successor not in in_fringe:
                fringe.push((successor, actions + [action]))
                in_fringe.add(successor)
                generated.append(successor)

        frontier_after = _frontier_states(fringe)
        parent = actions[-1] if actions else 'Start'
        _log_row(writer, iteration, state, parent,
                 actions[-1] if actions else 'None', generated,
                 frontier_before, frontier_after, explored)

    csv_file.close()
    return []

"""
HOW BFS WORKS:
BFS uses a queue (FIFO) so nodes are expanded in the order they were discovered —
level by level. This guarantees the shallowest (fewest-action) path on unweighted
graphs. A separate in_fringe set prevents enqueuing duplicates, and the explored
set ensures we never re-expand a state. The path list is carried with each node.
"""


# ---------------------------------------------------------------------------
# 3. Uniform-Cost Search
# ---------------------------------------------------------------------------

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    csv_file, writer = _init_csv('ucs')

    fringe = util.PriorityQueue()
    start = problem.getStartState()
    fringe.push((start, [], 0), 0)
    # best_g tracks the cheapest g-cost we've pushed for each state.
    # This acts as decrease-key: we only push if we found a strictly cheaper path.
    best_g = {start: 0}
    explored = set()
    iteration = 0

    while not fringe.isEmpty():
        state, actions, g = fringe.pop()

        if problem.isGoalState(state):
            iteration += 1
            _log_row(writer, iteration, state, '', '', [],
                     _frontier_states(fringe), _frontier_states(fringe),
                     explored, g, '', g)
            csv_file.close()
            return actions

        # Lazy deletion: skip if we already expanded this state
        if state in explored:
            continue

        explored.add(state)
        iteration += 1
        frontier_before = _frontier_states(fringe)

        successors_raw = problem.getSuccessors(state)
        generated = []
        for successor, action, step_cost in successors_raw:
            new_g = g + step_cost
            if successor not in explored:
                if successor not in best_g or new_g < best_g[successor]:
                    best_g[successor] = new_g
                    fringe.push((successor, actions + [action], new_g), new_g)
                    generated.append(successor)

        frontier_after = _frontier_states(fringe)
        parent = actions[-1] if actions else 'Start'
        _log_row(writer, iteration, state, parent,
                 actions[-1] if actions else 'None', generated,
                 frontier_before, frontier_after, explored, g, '', g)

    csv_file.close()
    return []

"""
HOW UCS WORKS:
UCS is like BFS but uses a priority queue ordered by cumulative path cost g(n)
instead of FIFO order. It always expands the cheapest-to-reach node first,
guaranteeing optimality even with non-uniform step costs. We track the best g-cost
per state (best_g) as a logical decrease-key: when a cheaper path is found, we
push the new entry and the old stale one is skipped at pop-time (lazy deletion).
"""


# ---------------------------------------------------------------------------
# 4. Greedy Best-First Search
# ---------------------------------------------------------------------------

def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node with the lowest heuristic value first."""
    csv_file, writer = _init_csv('gbfs')

    fringe = util.PriorityQueue()
    start = problem.getStartState()
    h_val = heuristic(start, problem)
    fringe.push((start, []), h_val)
    explored = set()
    in_fringe = set()
    in_fringe.add(start)
    iteration = 0

    while not fringe.isEmpty():
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            h_val = heuristic(state, problem)
            iteration += 1
            _log_row(writer, iteration, state, '', '', [],
                     _frontier_states(fringe), _frontier_states(fringe),
                     explored, '', h_val, '')
            csv_file.close()
            return actions

        if state in explored:
            continue

        explored.add(state)
        iteration += 1
        h_val = heuristic(state, problem)
        frontier_before = _frontier_states(fringe)

        successors_raw = problem.getSuccessors(state)
        generated = []
        for successor, action, cost in successors_raw:
            if successor not in explored and successor not in in_fringe:
                h_succ = heuristic(successor, problem)
                fringe.push((successor, actions + [action]), h_succ)
                in_fringe.add(successor)
                generated.append(successor)

        frontier_after = _frontier_states(fringe)
        parent = actions[-1] if actions else 'Start'
        _log_row(writer, iteration, state, parent,
                 actions[-1] if actions else 'None', generated,
                 frontier_before, frontier_after, explored, '', h_val, '')

    csv_file.close()
    return []

"""
HOW GBFS WORKS:
Greedy Best-First Search uses a priority queue ordered solely by the heuristic
h(n) — the estimated cost from the current state to the goal. It ignores the
cost already incurred (g), so it aggressively chases whichever state *looks*
closest to the goal. This makes it fast but NOT optimal — it can be misled by
heuristic traps where h underestimates a dead-end path.
"""


# ---------------------------------------------------------------------------
# 5. A* Search
# ---------------------------------------------------------------------------

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    csv_file, writer = _init_csv('astar')

    fringe = util.PriorityQueue()
    start = problem.getStartState()
    h_val = heuristic(start, problem)
    fringe.push((start, [], 0), 0 + h_val)
    best_g = {start: 0}
    explored = set()
    iteration = 0

    while not fringe.isEmpty():
        state, actions, g = fringe.pop()

        if problem.isGoalState(state):
            h_val = heuristic(state, problem)
            iteration += 1
            _log_row(writer, iteration, state, '', '', [],
                     _frontier_states(fringe), _frontier_states(fringe),
                     explored, g, h_val, g + h_val)
            csv_file.close()
            return actions

        if state in explored:
            continue

        explored.add(state)
        iteration += 1
        h_val = heuristic(state, problem)
        frontier_before = _frontier_states(fringe)

        successors_raw = problem.getSuccessors(state)
        generated = []
        for successor, action, step_cost in successors_raw:
            new_g = g + step_cost
            if successor not in explored:
                if successor not in best_g or new_g < best_g[successor]:
                    best_g[successor] = new_g
                    h_succ = heuristic(successor, problem)
                    f_val = new_g + h_succ
                    fringe.push((successor, actions + [action], new_g), f_val)
                    generated.append(successor)

        frontier_after = _frontier_states(fringe)
        parent = actions[-1] if actions else 'Start'
        _log_row(writer, iteration, state, parent,
                 actions[-1] if actions else 'None', generated,
                 frontier_before, frontier_after, explored,
                 g, h_val, g + h_val)

    csv_file.close()
    return []

"""
HOW A* WORKS:
A* combines the actual path cost g(n) with the heuristic estimate h(n) to form
f(n) = g(n) + h(n). It expands the node with the lowest f-value first. As long
as h is admissible (never overestimates) and consistent (satisfies the triangle
inequality), A* is guaranteed to find the optimal path while expanding fewer
nodes than UCS because the heuristic steers it toward the goal.
"""


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch
