# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    """Use the common implementation of Graph Search with the bag = Stack {LIFO}"""
    from util import Stack
    visited = []
    stack = Stack()
    stackElem = (problem.getStartState(),[])
    stack.push(stackElem)
    output = graphSearch(stack,problem,visited)
    return output

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    """Use the common implementation of Graph Search with the bag = Queue {FIFO}"""
    from util import Queue
    visited = []
    q = Queue()
    queueElem = (problem.getStartState(),[])
    q.push(queueElem)
    output = graphSearch(q,problem,visited)
    return output
    #util.raiseNotDefined()

def graphSearch(bag, problem, v):
    '''Set start = 0 to deal with the special case of only position being added (without direction), which only happens in the start state.'''
    start = 0
    while True:
        '''If bag is empty, search has failed. Return empty path.'''
        if bag.isEmpty():
            return []
        currState, currPath = bag.pop()
        if start==0:
            '''Start state, must be handled specially'''
            currPos = currState
            start = 1
        else:
            '''Any other state will have position, direction, and cost'''
            currPos = currState[0]
        '''Check if current position is Goal. If yes, return the current Path'''
        if problem.isGoalState(currPos):
            return currPath
        '''Check if currPos is not in visited. If not, mark it visited, and then expand it by adding its succesors.'''
        if currPos not in v:
            v.append(currPos)
            for suc in problem.getSuccessors(currPos):
                '''Extract position and path from successor. New path will be current path + successor path.'''
                sucPos = suc[0]
                sucPath = suc[1]
                newpath = currPath+[sucPath]
                stackElem = (suc,newpath)
                '''If the element isn't already in bag, add the element to bag.'''
                if stackElem not in bag.list:
                    bag.push(stackElem)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    if problem.isGoalState(state):
        return []

    closed = []
    path = ''
    pq = util.PriorityQueue()
    pq.push((state, 0, path), 0)
    while not pq.isEmpty():
        dequeued_node = pq.pop()
        curr_state = dequeued_node[0]
        curr_state_weight = dequeued_node[1]
        curr_path = dequeued_node[2]
        if problem.isGoalState(curr_state):
            return curr_path.strip().split(' ')

        if curr_state not in closed:
            successors = problem.getSuccessors(curr_state)
            closed.append(curr_state)
            for successor in successors:
                successor_state = successor[0]
                successor_action = successor[1]
                successor_cost = successor[2]
                cost = curr_state_weight + successor_cost
                complete_successor_action = curr_path + ' ' + successor_action
                if successor_state not in closed:
                    pq.push((successor_state, cost, complete_successor_action), cost)
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    state = problem.getStartState()
    """ If the starting state is the goal state, return empty path"""
    if problem.isGoalState(state):
        return []

    """Initialize closed list. This contains the list of explored nodes"""
    closed = []
    path = ''
    pq = util.PriorityQueue()
    pq.push((state, 0, path), 0)
    while not pq.isEmpty():
        dequeued_node = pq.pop()
        curr_state = dequeued_node[0]
        curr_state_weight = dequeued_node[1]
        curr_path = dequeued_node[2]
        if problem.isGoalState(curr_state):
            return curr_path.strip().split(' ')

        if curr_state not in closed:
            successors = problem.getSuccessors(curr_state)
            closed.append(curr_state)
            for successor in successors:
                successor_state = successor[0]
                successor_action = successor[1]
                successor_cost = successor[2]
                cost = curr_state_weight + successor_cost + heuristic(successor_state, problem)
                complete_successor_action = curr_path + ' ' + successor_action
                if successor_state not in closed:
                    pq.push((successor_state, curr_state_weight + successor_cost, complete_successor_action), cost)
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
