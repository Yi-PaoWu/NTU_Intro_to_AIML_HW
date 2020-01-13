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

def graphSearch(problem, search):

    "*** === Depth First Search ===== ***"

    if(search == 'dfs'):
        frontier = util.Stack()
        frontier.push(problem.getStartState())
        explored = set()
        actionList = []
        transitionTable = dict()
        node = problem.getStartState()
        
        goal = problem.getStartState()
        while(True):
            if (frontier.isEmpty()):
                break
            #leaves.append(problem.getSuccessors(problem.getStartState()))
            node = frontier.pop()
            #print node
            if(problem.isGoalState(node)):
                goal = node
            #    print "Goal : ", goal
            explored.add(node)
            leaves = []
            for j in problem.getSuccessors(node):

                if(not(j[0] in explored) and not(j[0] in frontier.list)):
                    frontier.push(j[0])
                if(not(j[0] in explored)):
                    transitionTable[j[0]] = (node,j[1])
        #print "transtionTable : ", transitionTable
        while(goal != problem.getStartState()):
            actionList.insert(0,transitionTable[goal][1])
            goal = transitionTable[goal][0]
        return actionList
            

        "*** === Breath First Search ===== ***"

    elif(search == 'bfs'):
        frontier = util.Queue()
        frontier.push(problem.getStartState())
        explored = set()
        actionList = []
        transitionTable = dict()
        node = problem.getStartState()
        goal = problem.getStartState()
        while(True):
            if (frontier.isEmpty()):
                break
            #leaves.append(problem.getSuccessors(problem.getStartState()))
            node = frontier.pop()
            #print "node : " ,node
            if(problem.isGoalState(node)):
                goal = node
                print "Goal : ", goal
                break
            explored.add(node)
            leaves = []
            for j in problem.getSuccessors(node):
                #leaves.append(problem.getSuccessors(node)[j][0])
            #print "leaves", leaves
           
                if(not(j[0] in explored) and not(j[0] in frontier.list)):
                    frontier.push(j[0])
         
                
                if(not(j[0] in explored)):
                    transitionTable[j[0]] = (node,j[1])
       
        while(goal != problem.getStartState()):
            actionList.insert(0,transitionTable[goal][1])
            goal = transitionTable[goal][0]
        return actionList

        "*** === Uniform Cost Search ===== ***"
        
    elif(search == 'ucs'):
        frontier = util.PriorityQueue()
        
        frontier.push(problem.getStartState(), 0)
        explored = set()
        actionList = []
        transitionTable = dict()
        node = problem.getStartState()
        
    
        state_dict = {problem.getStartState() : 0}
        while(True):
            if (frontier.isEmpty()):
                break
            node = frontier.pop()
            explored.add(node)

            if(problem.isGoalState(node)):    
                goal = node

            for j in problem.getSuccessors(node):
                if not(j[0] in explored) :
                    frontier.update(j[0],state_dict[node]+j[2])
                    if not state_dict.has_key(j[0]):
                        state_dict[j[0]] = state_dict[node] + j[2]
                    else :
                        if state_dict[j[0]] >  state_dict[node] + j[2]:
                            state_dict[j[0]] = state_dict[node] + j[2]
        
                for i in range(len(j)) :
                    if(not(j[0] in explored)):
                        transitionTable[j[0]] = (node,j[1])

        while(goal != problem.getStartState()):
            actionList.insert(0,transitionTable[goal][1])
            goal = transitionTable[goal][0]
        return actionList
        
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return graphSearch(problem,'dfs')

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return graphSearch(problem,'bfs')
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return graphSearch(problem,'ucs')
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
        
    frontier.push(problem.getStartState(),heuristic(problem.getStartState(), problem))
    explored = set()
    actionList = []
    transitionTable = dict()
    node = problem.getStartState()
        
    state_dict = {node : 0}
    while(True):
        if (frontier.isEmpty()):
            break
        #leaves.append(problem.getSuccessors(problem.getStartState()))
        node = frontier.pop()

        #print "node :", node, "f(n) : ",state_dict[node]

        if(problem.isGoalState(node)):    
            goal = node
            break
        #    print "Goal : ", goal
        explored.add(node)
        inFrontier = False
        for j in problem.getSuccessors(node):
            #print "node :", node[0], "f(n,node) : ",heuristic(node,problem),"leaf :",j[0]," heuristic: ",heuristic(j[0],problem)
                
            if not(j[0] in explored):
                frontier.update(j[0],state_dict[node]+j[2]+heuristic(j[0],problem))

                if not state_dict.has_key(j[0]):
                    state_dict[j[0]] = state_dict[node]+j[2]
                else:
                    if state_dict[j[0]]>state_dict[node]+j[2]:
                        state_dict[j[0]] = state_dict[node]+j[2]

             

            for i in range(len(j)) :
                if(not(j[0] in explored)):
                    transitionTable[j[0]] = (node,j[1])
    while(goal != problem.getStartState()):
        actionList.insert(0,transitionTable[goal][1])
        goal = transitionTable[goal][0]
    return actionList
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch















"""explored = set()
actionList = []
transitionTable = dict()
node = problem.getStartState()

goal = problem.getStartState()
while(True):
    if (frontier.isEmpty()):
        break
    #leaves.append(problem.getSuccessors(problem.getStartState()))
    node = frontier.pop()
    #print node
    if(problem.isGoalState(node)):
        goal = node
    #    print "Goal : ", goal
    explored.add(node)
    leaves = []
    for j in range(len(problem.getSuccessors(node))):
        leaves.append(problem.getSuccessors(node)[j][0])
    #print "leaves", leaves
    for leaf in leaves :
        if(not(leaf in explored) and not(leaf in frontier.list)):
            frontier.push(leaf)
    #print "frontier : ", frontier.list
    #print "explored : ", explored
    
    for i in range(len(problem.getSuccessors(node))) :
        if(not(problem.getSuccessors(node)[i][0] in explored)):
            transitionTable[problem.getSuccessors(node)[i][0]] = (node,problem.getSuccessors(node)[i][1])
#print "transtionTable : ", transitionTable
from game import Directions
s = Directions.SOUTH
w = Directions.WEST
n = Directions.NORTH
e = Directions.EAST
while(goal != problem.getStartState()):
    
    if (transitionTable[goal][1] == 'North'):
        actionList.insert(0,n)
    elif(transitionTable[goal][1] == 'South'):
        actionList.insert(0,s)
    elif(transitionTable[goal][1] == 'West'):
        actionList.insert(0,w)
    elif(transitionTable[goal][1] == 'East'):
        actionList.insert(0,e)
    goal = transitionTable[goal][0]
    #print "actionList : ", actionList

return actionList"""