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
import math
from util import manhattanDistance
from game import Directions
import random, util
from game import Grid

from game import Agent

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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        print "***********************time to move********************"
        print "i choose :",legalMoves[chosenIndex]
        print "\n"
        # input("okay ?")
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
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        """my pesudo code :
            monsters = getMonsters
            pellets = getFood
            d2m = 0
            d2f = 0
            for monster in monsters :
                d2m += 1.0/(distanceTo(monster)+1)
            for pellet in pellets :
                d2f += 1.0/(distanceTo(pellet)+1)
            some constraint on nextMove
            score d2m+d2f

        """
        print "#####DEBUG#####"
        d2m, d2f, score, foodMap, monsterMap = 0, 0, 0, [], []

        """calculate the average distance between pacman and monsters"""
        for position in successorGameState.getGhostPositions():
            monsterMap.append(position)
            d2m += 1.0/(util.manhattanDistance(position, newPos)+1)

        """Build a food map"""
        newFoodData= newFood.packBits()
        width, heigh = newFoodData[0], newFoodData[1]
        for y in range(heigh-1,-1,-1):
            for x in range(width):
                if newFood[x][y] == True:
                    foodMap.append((x,y))
        #print "food map :",foodMap

        """calculate the average distance between pacman and food"""
        for pellet in foodMap:
            d2f += 1.0/(util.manhattanDistance(newPos,pellet)+1)

        """calculate score"""
        score = d2f + d2m

        """if a pellet is in the new pos"""
        if oldFood.count() > newFood.count():
            print "foooood !!!"
            score = 99

        """not recommened to stay at the same pos"""
        if  newPos == currentGameState.getPacmanPosition():
            print "Get out there !"
            score -= 0.5


        """if a monster is in the new pos"""
        print "monsters are in:",monsterMap
        if newPos in monsterMap:
            print "monster !!!!!"
            score = -99

        """do not head towards a monster"""
        if d2m >= 0.5:
            print "not going to die today"
            score -= 10


        """if a monster is next to me this is also bad"""
        if newPos == currentGameState.getPacmanPosition():
            if d2m >= 0.5:
                print "not staying here man !"
                score = -99


        """print them to debug them"""
        print "cur pos =",currentGameState.getPacmanPosition()
        print "new pos=",newPos
        # print "food map =",foodMap
        # print "monster map=",monsterMap
        print "d2f =",d2f
        print "d2m =",d2m
        print "score =",score


        # input("okay?")
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

        bestScore, bestAction = self.max_value(gameState, 0)

        return bestAction


    def value(self, gameState, index, depth):

        value = 0
        action = ""
        if index == 0:
            if depth == self.depth:
                #terminal node
                value = self.evaluationFunction(gameState)
            else:
                #pacman turn
                value, action = self.max_value(gameState, depth)

        else:
            #agent
            # if depth == self.depth and index == (gameState.getNumAgents()-1):
            #     #terminal node
            #     value = 99999
            #     for action in gameState.getLegalActions(index):
            #         value = min(value, self.evaluationFunction(gameState.generateSuccessor(index, action)))
            #
            # else :
            value, action = self.min_value(gameState, index, depth)

            # print "index =", index, "depth :", depth, "value :", value
            # input("okay ?")
        return value


    def max_value(self, gameState, depth):

        """
        depth += 1
        value = inf
        bestAction = null
        for action in availableActions:
            newValue = successor(index, action)
            if newValue > value:
                value = newValue
                bestAction = action
        return value, bestAction

        :param gameState: the current state
        :param depth: the current depth
        :return: the max action and its value
        """
        depth += 1
        value = -99999
        bestAction = ""
        for action in gameState.getLegalActions(0):
            newValue = self.value(gameState.generateSuccessor(0, action), (1)%gameState.getNumAgents(), depth)
            if newValue > value:
                value = newValue
                bestAction = action
        # print "MAX at depth :", depth, "value :", value
        #input("okay ?")
        if bestAction =="":
            value = self.evaluationFunction(gameState)
        return value, bestAction



    def min_value(self, gameState, index, depth):
        """
        value = -inf
        bestAction = null
        for action in availableActions:
            newValue = successor(index, action)
            if newValue < value:
                value = newValue
                bestAction = action
        return value, bestAction

        :param gameState: the current state
        :param index: the agent index
        :param depth: the current depth
        :return: the min action and its value
        """

        value = 99999
        bestAction = ""
        for action in gameState.getLegalActions(index):
            newValue = self.value(gameState.generateSuccessor(index,action), (index+1)%gameState.getNumAgents(), depth)
            if newValue < value:
                value = newValue
                bestAction = action
        # print "index =", index, "depth :", depth, "value :", value
        #input("okay ?")
        if bestAction =="":
            value = self.evaluationFunction(gameState)
        return value, bestAction



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        bestScore, bestAction = self.max_value(gameState, 0,-99999,99999)

        return bestAction

    def value(self, gameState, index, depth, alpha, beta):

        value = 0
        action = ""
        if index == 0:
            if depth == self.depth:
                #terminal node
                value = self.evaluationFunction(gameState)
            else:
                #pacman turn
                value, action = self.max_value(gameState, depth, alpha, beta)

        else:
            #agent
            # if depth == self.depth and index == (gameState.getNumAgents()-1):
            #     #terminal node
            #     value = 99999
            #     for action in gameState.getLegalActions(index):
            #         value = min(value, self.evaluationFunction(gameState.generateSuccessor(index, action)))
            #
            # else :
            value, action = self.min_value(gameState, index, depth, alpha, beta)

            # print "index =", index, "depth :", depth, "value :", value
            # input("okay ?")
        return value


    def max_value(self, gameState, depth, alpha, beta):

        depth += 1
        value = -99999
        bestAction = ""
        for action in gameState.getLegalActions(0):
            newValue = self.value(gameState.generateSuccessor(0, action), (1)%gameState.getNumAgents(), depth, alpha, beta)
            if newValue > value:
                value = newValue
                bestAction = action
            if newValue > alpha :
                alpha = newValue
            if newValue > beta:
                return newValue, bestAction
        # print "MAX at depth :", depth, "value :", value
        #input("okay ?")
        if bestAction =="":
            value = self.evaluationFunction(gameState)
        return value, bestAction



    def min_value(self, gameState, index, depth, alpha, beta):
        value = 99999
        bestAction = ""
        for action in gameState.getLegalActions(index):
            newValue = self.value(gameState.generateSuccessor(index,action), (index+1)%gameState.getNumAgents(), depth, alpha, beta)
            if newValue < value:
                value = newValue
                bestAction = action
            if newValue < beta :
                beta = newValue
            if newValue < alpha:
                return newValue, bestAction
        # print "index =", index, "depth :", depth, "value :", value
        #input("okay ?")
        if bestAction =="":
            value = self.evaluationFunction(gameState)
        return value, bestAction

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
        bestScore, bestAction = self.max_value(gameState, 0)

        return bestAction


    def value(self, gameState, index, depth):

        value = 0
        action = ""
        if index == 0:
            if depth == self.depth:
                #terminal node
                value = self.evaluationFunction(gameState)
            else:
                #pacman turn
                value, action = self.max_value(gameState, depth)

        else:

            value = self.min_value(gameState, index, depth)

        return value


    def max_value(self, gameState, depth):

        depth += 1
        value = -99999
        bestAction = ""
        for action in gameState.getLegalActions(0):
            newValue = self.value(gameState.generateSuccessor(0, action), (1)%gameState.getNumAgents(), depth)
            if newValue > value:
                value = newValue
                bestAction = action
        # print "MAX at depth :", depth, "value :", value
        #input("okay ?")
        if bestAction =="":
            value = self.evaluationFunction(gameState)
        return value, bestAction



    def min_value(self, gameState, index, depth):

        value = .0
        counter = .0
        for action in gameState.getLegalActions(index):
            newValue = self.value(gameState.generateSuccessor(index,action), (index+1)%gameState.getNumAgents(), depth)
            value += newValue
            counter += 1
        # print "index =", index, "depth :", depth, "value :", value
        #input("okay ?")

        value = value*1.0/(counter+1)

        return value

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    # print "#####DEBUG#####"
    d2m, d2f, score, foodMap, monsterMap = 0, 0, 0, [], []

    """calculate the average distance between pacman and monsters"""
    for position in currentGameState.getGhostPositions():
        monsterMap.append(position)
        d2m += 1.0 / (util.manhattanDistance(position, newPos) + 1)

    """Build a food map"""
    newFoodData = newFood.packBits()
    width, heigh = newFoodData[0], newFoodData[1]
    for y in range(heigh - 1, -1, -1):
        for x in range(width):
            if newFood[x][y] == True:
                foodMap.append((x, y))
    # print "food map :",foodMap

    """calculate the average distance between pacman and food"""
    for pellet in foodMap:
        d2f += 1.0 / 100*(util.manhattanDistance(newPos, pellet) + 1)

    myAgent = ExpectimaxAgent()
    expect_value = ExpectimaxAgent.value(myAgent, currentGameState,0,0)

    """calculate score"""
    score = d2f + d2m + expect_value

    # print "d2f =", d2f
    # print "d2m =", d2m
    # print "excpect_value =",expect_value
    # print "score =", score

    # input("okay?")
    return score



# Abbreviation
better = betterEvaluationFunction

