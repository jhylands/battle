'''
This module handle the game strategy (only) of a player.

Created on 7 Aug 2014

@author: Lilian
'''

from random import randint
import const
import time
# The variable representing our game board, containing our fleet and the moves made by the opponent.
playerBoard = None

# The variable representing the opponent game board, containing the moves we have made.
opponentBoard = None

# The variable representing our next targets
targets = [{'x': 5 ,'y': 5 }]

# The variable representing the result of our last shot so we can use it in our desition
confirmShot = {'killed' : const.EMPTY}

#make a function to validate that a set of coordinates are on the L shaped board
def XYValid(x,y):
    if ((x>=0) and (y>=0) and (x<12 and y<12)) and ((x>5 and y>5) or (y<6)):
	return True
    else:
	return False
#confirm the square has not already been guessed at 
def noSecondGuess(x,y,board,targets):
    ToReturn = False
    try:
	if targets.index({'x' : x, 'y' : y}) >-1:
	    print 'Already in list'
    except:
	if board[x][y]==const.EMPTY:
	    ToReturn = True
    return ToReturn
#make a function to initiate the list of guesses
def initGuessList():
    for i in range(0,11,2):
	for n in range(0,11,2):
	    if XYValid(n,i):
		guessList.append({'x' : n, 'y' : i})
    for i in range(1,11,2):
	for n in range(1,11,2):
	    if XYValid(n,i):
		guessList.append({'x' : n, 'y' : i})

# Make a list of the sensible places to gues
guessList = []
initGuessList() 	    
# Enter your own player name
playerName = "Crawler" 

# Enter your own player description, e.g. what kind of strategy has been used.
playerDescription = "Moves are chosen randomly on a chessboard until a hit then the algo crawls along the hit looking for other hits"
            

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
    
    # Destroyer (2 squares)
    playerBoard[0][5]=const.OCCUPIED
    playerBoard[1][5]=const.OCCUPIED
    
    # Cruiser (3 squares)
    playerBoard[1][1:4]=[const.OCCUPIED]*3
    
    # Battleship (4 squares)
    playerBoard[6][6]=const.OCCUPIED
    playerBoard[6][7]=const.OCCUPIED
    playerBoard[6][8]=const.OCCUPIED
    playerBoard[6][9]=const.OCCUPIED
    
    # Hovercraft (6 squares)
    playerBoard[8][2]=const.OCCUPIED
    playerBoard[9][1:4]=[const.OCCUPIED]*3
    playerBoard[10][1:4:2]=[const.OCCUPIED]*2
    
    # Aircraft carrier (6 squares)
    playerBoard[9][5:9]=[const.OCCUPIED]*4
    playerBoard[8][5]=const.OCCUPIED
    playerBoard[10][5]=const.OCCUPIED
    return playerBoard

def chooseMove():
    """
    Should Decide what move to make based on current state of opponent's board and return it 
    # currently Completely random strategy,
    # Knowledge about opponent's board is completely ignored (hence the name of the player),
    # You definitely want to change that.
    """
    global playerBoard, opponentBoard, targets, confirmShot, guessList
    #if we just got a hit add the surrounding blocks as educated guesses to targets array
    if confirmShot['killed'] == const.HIT:
	for rack in opponentBoard:
		print rack
	#time.sleep(1)
	counter = 0
	print 'Confirmed kill at: (' + str(confirmShot['x']) + "," + str(confirmShot['y']) + ')'
	i = range(-1,2)
	for Xer in i:
		for Yer in i:
			x = confirmShot['x'] + Xer
			y = confirmShot['y'] + Yer	
			counter = counter + 1
			if XYValid(x,y):
			    if noSecondGuess(x,y,opponentBoard,targets):
				 targets.append({'x': x, 'y' : y})
				

	if counter < 9:
	    print counter
	    time.sleep(20)
#			#check their not bellow zero and not in the L bit and they are both less that 12

#				try:
#				    if opponentBoard[x][y] == const.EMPTY:
#					try:
#						print targets.index({'x' : x, 'y': y})
#						print 'Already in list'
#						time.sleep(2)
#						break
#					except:
#						#add that
#						 print "Adding:(" + str(x) + "," + str(y) + ") to the list of possible targets"
#				    break
#				except IndexError:
#					 #if for some reason a guess is not on the board
#					 print 'ERROR: ' + str(x) + ":" + str(y) + 'out of range'
#   
    #if we haven't got any educated guesses make a random one
    if len(targets)==0:
	    targets.append(guessList.pop())
	    print 'Random target selected!'
    try:
	target = targets.pop()
    except IndexError:
	target = {'x' : 5, 'y' : 5}	
	print 'pop ERROR!'
    print 'Targets length:' + str(targets)
    #time.sleep(3)
    return target['x'],target['y']

def setOutcome(entry, i1, i2):
    """
    Receives the outcome of the shot
    expected value is const.HIT for hit and const.MISSED for missed
    """
    global playerBoard, opponentBoard, confirmShot
    confirmShot['killed'] = entry
    confirmShot['x'] = i1
    confirmShot['y'] = i2
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
    initGuessList()

def newPlayer():
    """
    This method is used for backward compatibility. It will not be used during the competition. 
    You should ignore this function.
    """
    pass
