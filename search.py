# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()


def getCostOfActions(self, actions):
    """
    actions: A list of actions to take

    This method returns the total cost of a particular sequence of actions.
    The sequence must be composed of legal moves
    """
    util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


class Node:
    """Defines a simple search node that does not track the cost of
    the current search path.
    """

    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

    def __eq__(self, node):
        return node.state == self.state


def search(problem, strategy):
    """A generic search algorithm that can be used by DFS and BFS."""
    node = Node(problem.getStartState(), [])
    explored = set()
    strategy.push(node)
    while strategy:
        node = strategy.pop()
        if problem.isGoalState(node.state):
            return node.actions
        explored.add(node.state)
        for s, a, c in problem.getSuccessors(node.state):
            child = Node(s, node.actions+[a])
            if s not in explored and child not in strategy:
                strategy.push(child)
    return []


class CostNode:
    """Defines a simple search node that tracks the cost of the search path."""

    def __init__(self, state, actions, gcost, hcost=0):
        self.state = state
        self.actions = actions
        self.gcost = gcost
        self.hcost = hcost
        self.fcost = gcost + hcost

    def __eq__(self, node):
        return node.state == self.state

    def __le__(self, node):
        return node.fcost <= self.fcost

    def __lt__(self, node):
        return node.fcost < self.fcost

    def __ge__(self, node):
        return node.fcost >= self.fcost

    def __gt__(self, node):
        return node.fcost > self.fcost


def cost_search(problem, heuristic=lambda x,y: 0):
    """A generic search algorithm that can be used by UCS or a-star."""

    start = problem.getStartState()
    frontier = util.PriorityQueue()
    counter = 0
    frontier.push((start, [], 0), (heuristic(start, problem), counter))
    best_cost = {start: 0}

    while not frontier.isEmpty():
        state, actions, gcost = frontier.pop()

        # Skip stale entries that are not the best known path to this state.
        if gcost > best_cost.get(state, float('inf')):
            continue

        # Goal test must happen when a node is removed from the frontier.
        if problem.isGoalState(state):
            return actions

        for succ, action, step_cost in problem.getSuccessors(state):
            new_g = gcost + step_cost
            if new_g < best_cost.get(succ, float('inf')):
                best_cost[succ] = new_g
                counter += 1
                fcost = new_g + heuristic(succ, problem)
                frontier.push((succ, actions + [action], new_g), (fcost, counter))
    return []


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    """
    Question1:
    My explanation:
    stack follows LIFO (Last in first out). So, the last node added is the first
    one removedBecause of this, the search keeps going deeper along one branch
    first before coming back to explore other branches. This is why it behaves
    like Depth-First Search.
    """
    fringe = util.Stack()
    fringe.push((problem.getStartState(), []))
    explored = set()

    while len(fringe):
        state, actions = fringe.pop()

        if problem.isGoalState(state):
            return actions

        if state in explored:
            continue

        explored.add(state)
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in explored:
                fringe.push((successor, actions + [action]))

    return []


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """

    """
    Question 2:
    My explanation:
    A queue follows FIFO (First In, First Out). The first node added is the first
    one removed. Because of this, the search explores all nodes at one level before
    moving to the next level. This is why it behaves like Breadth-First Search.
    
    """
    return search(problem, util.Queue())


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    """
    Question 3:
    My explanation:
    Uniform Cost Search (UCS) uses a priority queue that always picks the node with
    the lowest total cost so far. This means the algorithm always explores the
    cheapest path first, which helps it find the best solution when costs are not
    negative. The goal is checked when a node is removed from the queue, because at
    that point we know no cheaper path to that state exists. If a cheaper path to a
    state is found later, the algorithm updates the queue and replaces the older
    expensive path so it doesn't expand a worse one.
    """
    return cost_search(problem)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    """
    A star algorithm finds the same optimal path as BFS/UCS but expands far fewer nodes because
    Manhattan distance guides it in a straight line toward the goal in the open space.
    """
    return cost_search(problem, heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
