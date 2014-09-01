'''
This module handle the game strategy (only) of a player.

Created on 7 Aug 2014

@author: Lilian
'''

from random import randint
import const

# The variable representing our game board, containing our fleet and the moves made by the opponent.
playerBoard = None

# The variable representing the opponent game board, containing the moves we have made.
opponentBoard = None

# Enter your own player name
playerName = "Dummy Player" 

# Enter your own player description, e.g. what kind of strategy has been used.
playerDescription = "Moves are chosen randomly, may hit the same place more than once."
            

def initBoards():                
    # Initially, the player's board is all empty, the opponent's is all unknown
    global playerBoard, opponentBoard
    
    playerBoard = [[const.EMPTY]*(6 if x<6 else 12) for x in range(12)]
    opponentBoard = [[const.EMPTY]*(6 if x<6 else 12) for x in range(12)]



# Distribute the fleet onto your board
def deployFleet():
    """
    Decide where you want your fleet to be deployed, then return your board. 
    """
    global playerBoard, opponentBoard
    
    initBoards()
    # Simple example which always positions the ships in the same place
    # This is a very bad idea! You will want to do something random
    for i in range(0,21):
	x=input('X:')
	y=input('y:')
	playerBoard[x][y]=const.OCCUPIED
    return playerBoard

def chooseMove():
    """
    Should Decide what move to make based on current state of opponent's board and return it 
    # currently Completely random strategy,
    # Knowledge about opponent's board is completely ignored (hence the name of the player),
    # You definitely want to change that.
    """
    global playerBoard, opponentBoard
    
    row = input('x:')
    col = input('y:')
    
    return row, col

def setOutcome(entry, i1, i2):
    """
    Receives the outcome of the shot
    expected value is const.HIT for hit and const.MISSED for missed
    """
    global playerBoard, opponentBoard
    if entry == const.HIT:
	print "Hit"
    else:
	print "miss"
    if entry == const.HIT or entry == const.MISSED:
        opponentBoard[i1][i2] = entry # record the result on the board
    else:
        raise Exception("Invalid input!")
    

def getOpponentMove(i1,i2):
    """ 
    You might like to keep track of where your opponent
    has missed/hit, but here we just acknowledge it
    """
    global playerBoard, opponentBoard
    
    if ((playerBoard[i1][i2]==const.OCCUPIED)
        or (playerBoard[i1][i2]==const.HIT)):
        # They may (stupidly) hit the same square twice so we check for occupied or hit
        playerBoard[i1][i2]=const.HIT
        result =const.HIT
    else:
        # You might like to keep track of where your opponent has missed, but here we just acknowledge it
        playerBoard[i1][i2]=const.MISSED
        result = const.MISSED
    return result

def newRound():
    """
    This method is called when a new round is starting (new game with same player). This gives you the 
    ability to update your strategy.
    Currently does nothing.
    """
    pass

def newPlayer():
    """
    This method is used for backward compatibility. It will not be used during the competition. 
    You should ignore this function.
    """
    pass
