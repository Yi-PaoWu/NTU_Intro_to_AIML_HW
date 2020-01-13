# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from game import Actions

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores =[]
        for action in legalMoves:
            scores.append(self.evaluationFunction(gameState, action))
            #print "the score of ",action," is ", self.evaluationFunction(gameState, action)
        #scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        #print "___________ END OF ONE ACTION _________"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghostPosition1 = newGhostStates[0].getPosition() 
        #ghostPosition2 = newGhostStates[1].getPosition()

        score = successorGameState.getScore()
        if newFood[newPos[0]][newPos[1]]:
            score += 1
        if newFood[newPos[0]+1][newPos[1]]:
            score += 0.6
        elif newFood[newPos[0]-1][newPos[1]]:
            score += 0.6
        elif newFood[newPos[0]][newPos[1]+1]:
            score += 0.6
        elif newFood[newPos[0]][newPos[1]-1]:
            score += 0.6
        if currentGameState.getPacmanPosition()[0] == newPos[0] and currentGameState.getPacmanPosition()[1] == newPos[1]:
            score -= 0.5
        foodList = newFood.asList()
        FoodDistance = [(manhattanDistance(food,newPos),food) for food in foodList]
        if len(FoodDistance) != 0:
            score += 1.5/min(FoodDistance[0])
            i_nearestFood = FoodDistance[0].index(min(FoodDistance[0]))
            for i in range(newPos[0],FoodDistance[i_nearestFood][1][0]):
                if successorGameState.getWalls()[i][newPos[1]] :
                    score -= 0.8
                    break
                    #print "YYYYYY"
            for j in range(newPos[1],FoodDistance[i_nearestFood][1][1]):     
                if successorGameState.getWalls()[newPos[0]][j] :
                    score -= 0.8
                    break
                    #print "XXXXX"

        
        if newScaredTimes[0] == 0 :
            if ghostPosition1 == newPos:
                #print  newPos,"ghostPosition (close!!):", ghostPosition1
                score -= 1500
            elif manhattanDistance(newPos,ghostPosition1) <=1:
                #print newPos,"ghostPosition :", ghostPosition1
                score -= 100
        #    if newPos[0] == ghostPosition2[0] and newPos[1] == ghostPosition2[1]:
        #       score -= 1500
        #    elif manhattanDistance(newPos,ghostPosition2) <=1:
                #print newPos,"ghostPosition :", ghostPosition1
                score -= 100
        elif newScaredTimes[0] >=2:
            if newPos[0] == ghostPosition1[0] and newPos[1] == ghostPosition1[1]:
                score += 300
            elif  manhattanDistance(newPos,ghostPosition1):
                score += 30
        #elif newScaredTimes[1] >=2:
        #    if newPos[0] == ghostPosition2[0] and newPos[1] == ghostPosition2[1]:
        #        score += 300
        #    elif  manhattanDistance(newPos,ghostPosition2):
        #        score += 30
            #if newPos[0] == ghostPosition2[0] and newPos[1] == ghostPosition2[1]:
            #   score -= 500
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0)
        print legalActions
        score = -999999
        n_action = 'Stop'
        for action in legalActions :
            temp = self.minimax(gameState.generateSuccessor(0,action),1,1)
        #   print "temp : ", temp
            if temp > score:
                score = temp
                n_action = action
        #print action
        #print score
        return n_action
        util.raiseNotDefined()

    def minimax(self,gameState,now_depth,agent):
             
        if now_depth == self.depth and agent == gameState.getNumAgents()-2: 
            legalActions = gameState.getLegalActions(agent)
            #print legalActions
            
            min_score = 99999999
            for action in legalActions:
                if self.evaluationFunction(gameState.generateSuccessor(agent,action)) < min_score :
                    min_score = self.evaluationFunction(gameState.generateSuccessor(agent,action))
            
            #print min_score
            if min_score != 99999999:
                return min_score
            else:
                return self.evaluationFunction(gameState)
        else :
            if agent == 0:   #PACMAN
                legalActions = gameState.getLegalActions(0) #find legal actions
                max_score = -999999
                
                for action in legalActions:
                    temp = self.minimax(gameState.generateSuccessor(0,action),now_depth,1)
                    if  temp > max_score :
                        max_score = temp
                if max_score != -999999:
                    return max_score
                else:
                    return self.evaluationFunction(gameState)
            else :          #GHOST
                legalActions = gameState.getLegalActions(agent)
                if agent == gameState.getNumAgents()-1 :
                    next_agent = 0
                    now_depth += 1
                else  :
                    next_agent = agent+1

                min_score = 99999999
                for action in legalActions:
                    temp = self.minimax(gameState.generateSuccessor(agent,action),now_depth,next_agent)
                    if  temp < min_score :
                        min_score = temp
                if min_score != 99999999:
                    return min_score
                else :
                    return self.evaluationFunction(gameState)
                    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalActions = gameState.getLegalActions(0)
        #print legalActions
        score = -999999999
        n_action = 'Stop'
        for action in legalActions :
            temp = self.alphabeta(gameState.generateSuccessor(0,action),1,1,-99999999,99999999)
            if temp > score:
                score = temp
                n_action = action
        #print score
        return n_action
        util.raiseNotDefined()


    def alphabeta(self, gameState, now_depth, agent, alpha, beta):
        if now_depth == self.depth and agent == gameState.getNumAgents()-2 :
            legalActions = gameState.getLegalActions(agent)
            min_score = 99999999
            for action in legalActions:
                if self.evaluationFunction(gameState.generateSuccessor(agent,action)) < min_score :
                    min_score = self.evaluationFunction(gameState.generateSuccessor(agent,action))
            if min_score != 99999999:
                return min_score
            else:
                return self.evaluationFunction(gameState)
        else :
            if agent == 0:
                v = -99999999
                legalActions = gameState.getLegalActions(agent)
                for action in legalActions:
                    temp  = self.alphabeta(gameState.generateSuccessor(agent,action), now_depth, 1, alpha, beta)
                    if  temp > v:
                        v = temp 
                    if v >= beta : return v
                    alpha = max(alpha,v)
                if v != -99999999:
                    return v
                else :
                    return self.evaluationFunction(gameState)
            else : 
                legalActions = gameState.getLegalActions(agent)
                if agent == gameState.getNumAgents()-1 :
                    next_agent = 0
                    now_depth += 1
                else  :
                    next_agent = agent+1
                v = 99999999
                for action in legalActions:
                    temp  = self.alphabeta(gameState.generateSuccessor(agent,action), now_depth, next_agent, alpha, beta)
                    if  temp < v:
                        v = temp 
                    if v <= alpha : return v
                    beta = min(beta, v)
                if v != 99999999:
                    return v
                else :
                    return self.evaluationFunction(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        legalActions = gameState.getLegalActions(0)
        #print legalActions
        score = -999999
        n_action = 'Stop'
        for action in legalActions :
            temp = self.expectiMinimax(gameState.generateSuccessor(0,action),1,1)
            #print "action = ", action, "score =", temp
            if temp >score :
                score = temp
                n_action = action
            elif temp == score and n_action == 'Stop' :
                score = temp
                n_action = action
           

        #print n_action
        #print "-------------------------------------"
        return n_action

        util.raiseNotDefined()


    def expectiMinimax(self, gameState, now_depth, agent):
        if now_depth == self.depth and agent == gameState.getNumAgents()-2: 
            legalActions = gameState.getLegalActions(agent)
            #print legalActions
            
            min_score = 99999999
            for action in legalActions:
                if self.evaluationFunction(gameState.generateSuccessor(agent,action)) < min_score :
                    min_score = self.evaluationFunction(gameState.generateSuccessor(agent,action))
            if min_score != 99999999:
                return min_score
            else:
                return self.evaluationFunction(gameState)
        else :
            if agent == 0:   #PACMAN
                legalActions = gameState.getLegalActions(0) #find legal actions
                max_score = -999999
                for action in legalActions:
                    #print "action = ", action
                    temp = self.expectiMinimax(gameState.generateSuccessor(0,action),now_depth,1)
                    #print "action = ", action, "score =", temp

                    if  temp >= max_score :
                        max_score = temp
                #print "------------------------------------"
                if max_score != -999999:
                    #print max_score
                    return max_score
                else:
                    return self.evaluationFunction(gameState)
            else :          #GHOST
                legalActions = gameState.getLegalActions(agent)
                if agent == gameState.getNumAgents()-1 :
                    next_agent = 0
                    now_depth += 1
                else  :
                    next_agent = agent+1
                if len(legalActions) != 0:
                    action = random.choice(legalActions)
                    return self.expectiMinimax(gameState.generateSuccessor(agent,action),now_depth,next_agent)
                else :
                    return self.evaluationFunction(gameState)
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      
      Function BFS_distance(currentGameState, x) : search for the distance of the neareat food from current position of pacman with up to x nodes 
        
      1) Search nearest food : Divide in to three cases
      -if the number of rest food is more than 30, then search BFS_distance with up to 20 nodes
      and the score += 8.0/(distance from nearest food) + 450.0/(number of total food) + 3*current_score

      -if the number of rest food is more than 12, then search_BFS distance with up to 256 nodes
      and the score += 8.0/(distance from nearest food) + 210.0/(number of total food) + 3*current_score

      -if the number of rest food is less than 12, then get manhattan distance from current position of pacman to nearest food
      and the score += 12.0/(manhattan distance of pacman and nearest food) + 105.0/(number of total food) + 3*current_score
        
      2) Search ghost :
      - if ghost is not scared : get manhattan distance of pacman and two ghosts, and deduct 1000,300,200,25 of score if manhattan distance is =1,=2,<4,<7 respectively
      - if ghost is scared : get manhattan distance of pacman and two ghosts, and add 500,200,75 of score if manhattan distance is =1,<3,<5 respectively

      3) Capsule :
      - if number of capsules = 1 , add 100 to score
      - if number of capsules = 0 , add 250 to score

      4) Special case of wall (avoid going into dead end) :
      - if there are three walls around pacman : deduct 30 of score

    """
    "*** YOUR CODE HERE ***"

    #### DECLARATION #####

    current_score = currentGameState.getScore()
    GhostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    food = currentGameState.getFood()
    foodList = food.asList()
    ghostPosition1 = currentGameState.getGhostPosition(1)
    ghostPosition2 = currentGameState.getGhostPosition(2)
    capsules = currentGameState.getCapsules()
    current_position = currentGameState.getPacmanPosition()
    walls = currentGameState.getWalls()
    score = 0
    wall_around = 0
    
    ##### SCORE OF FOOD DISTANCE AND getScore() #####

    if len(foodList) >= 30 :
        distance = BFS_distance(currentGameState, 30)
        #print distance
    elif len(foodList) >= 15 :
        distance = BFS_distance(currentGameState, 256)
        #print distance
    if len(foodList) >= 30 :
            score += 8.0/distance + 420.0/len(foodList) + 5*current_score
    elif len(foodList) >= 15 :
            score += 8.0/distance + 210.0/len(foodList) + 5*current_score
    else :
        FoodDistance = [(manhattanDistance(food,current_position),food) for food in foodList]
        min = 9999999
        if len(FoodDistance) != 0:  
            for i in FoodDistance :
                if i[0]< min :
                    min = i[0]
                    nearestFood = i[1]
            score += 12.0/min + 105.0/len(foodList) + 5*current_score

            for i in range(current_position[0],nearestFood[0]):
                if walls[i][current_position[1]] :
                    score -= 5
                    break
            for j in range(current_position[1],nearestFood[1]):     
                if walls[current_position[0]][j] :
                    score -= 5
                    break
        else :
            score += 10.0/min + 5*current_score

    if walls[current_position[0]+1][current_position[1]]:
        wall_around += 1
    if walls[current_position[0]][current_position[1]+1]:
        wall_around += 1
    if walls[current_position[0]-1][current_position[1]]:
        wall_around += 1
    if walls[current_position[0]][current_position[1]-1]:
        wall_around += 1

    if wall_around >= 3:
        score -= 30

    ##### SCORE OF GHOST ######    
           
    ghost1_distance = manhattanDistance(ghostPosition1,current_position)
    ghost2_distance = manhattanDistance(ghostPosition2,current_position)

    if len(capsules) ==  1:
        score += 100
    elif len(capsules) == 0:
        score += 250 

    if scaredTimes[0] <= 2 or scaredTimes[1] <= 2 :
        if scaredTimes[0] <= 2 : 
            if ghostPosition1 == current_position:
                score -= 1000
            elif ghost1_distance == 1:
                score -= 300
            elif ghost1_distance <4:
                score -= 200
            elif ghost1_distance <7:
                score -= 35
            
        if scaredTimes[1] <= 2 :
            if ghostPosition2 == current_position:
                score -= 1000
            elif ghost2_distance == 1:
                score -= 300
            elif ghost2_distance <4:
                score -= 200
            elif ghost2_distance <7:
                score -= 35     

    if scaredTimes[0] >= 2 and ghost1_distance == 0 :
        score += 500
    elif scaredTimes[0] >= 2 and ghost1_distance < 3:
        score += 200
    elif scaredTimes[0] >= 2 and ghost1_distance < 5:
        score += 75
    if scaredTimes[1] >= 2 and ghost2_distance == 0:
        score += 500
    elif scaredTimes[1] >= 2 and ghost2_distance < 3:
        score += 200
    elif scaredTimes[1] >= 2 and ghost2_distance < 5:
        score += 75
        
    return score
    util.raiseNotDefined()

def BFS_distance(currentGameState,depth):
    frontier = util.Queue()
    frontier.push(currentGameState.getPacmanPosition())
    explored = set()
    now_depth = 1
    score = 0
    food = currentGameState.getFood()
    foodList = food.asList()
    walls = currentGameState.getWalls()
    capsules = currentGameState.getCapsules()
    GhostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    actions = ['North', 'South', 'East', 'West']
    ghostPosition1 = currentGameState.getGhostPosition(1)
    ghostPosition2 = currentGameState.getGhostPosition(2)
    food_dict = dict()
    distance = 1
    goal = currentGameState.getPacmanPosition()
    while(True):
        if frontier.isEmpty():
            break
        node = frontier.pop()
        if  food[node[0]][node[1]] : 
            goal = node   
            break
        if now_depth == depth:
            break
        explored.add(node)
        x,y = node
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not walls[nextx][nexty] :
                if not (nextx,nexty) in explored and not (nextx,nexty) in frontier.list :
                    frontier.push((nextx,nexty))
                if not (nextx,nexty) in explored :
                    food_dict[(nextx,nexty)] = node
        now_depth += 1

    while(goal != currentGameState.getPacmanPosition()) :
        goal = food_dict[goal]
        distance += 1
    return distance

# Abbreviation
better = betterEvaluationFunction

