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

def initPlaceList():
    for i in range(0,11):
	for n in range(0,11):
	    if XYValid(n,i):
		guessList.append({'x' : n, 'y' : i})
#array of all the ships
ships =[]
#destroyer
ships.append([{'x' : 0, 'y' : 0},{'x' : 1, 'y' : 0}])
#cruiser
ships.append([{'x' : 0, 'y' : 0},{'x' : 1, 'y' : 0},{'x' : 2, 'y' : 0}])
#battleship
ships.append([{'x' : 0, 'y' : 0},{'x' : 1, 'y' : 0},{'x' : 2, 'y' : 0},{'x' : 3, 'y' : 0}])
#hovercraft
ships.append([{'x' : 0, 'y' : 0},{'x' : 1, 'y' : 0},{'x' : 1, 'y' : -1},{'x' : 1, 'y' : 1},{'x' : 2, 'y' : -1},{'x' : 2, 'y' : 1}])
#Aircraft carrier
ships.append([{'x' : 0, 'y' : 0},{'x' : 1, 'y' : 0},{'x' : 2, 'y' : 0},{'x' : 3, 'y' : 0},{'x' : 3, 'y' : -1},{'x' : 3, 'y' : 1}])
def getBoard(board):
	for ship in ships:
	    #chose random position
	    invalidPosition = True
	    placeList = initPlaceList()
	    while invalidPosition:
 		#place = placeList.pop()
		col = randint(0,len(board)-1)
		row = randint(0,len(board[col]))
		thisTrans=True
		#look to see if the position is valid
		for element in ship:
		    if not (XYValid(element['x']+col,element['y']+row)):
			    thisTrans = False
		    elif  not(board[element['x']+col][element['y']+row]==const.EMPTY):
    			    thisTrans = False
			    print 'Overlap len:' + str(len(board)) + ";" + str(col) + ":" + str(row)	
		if thisTrans:
		    invalidPosition = False
		    for element in ship:
			element['x'] = element['x']+col
			element['y'] = element['y']+row
			board[element['x']][element['y']] = const.OCCUPIED
	return board

# Make a list of the sensible places to gues
guessList = []
initGuessList() 	    
#Statistics
#get number of moves that are guesses
ges = 0
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
    for rack in playerBoard:
	print rack
    playerBoard = getBoard(playerBoard)
    for rack in playerBoard:
	print rack
    return playerBoard

def chooseMove():
    """
    Should Decide what move to make based on current state of opponent's board and return it 
    # currently Completely random strategy,
    # Knowledge about opponent's board is completely ignored (hence the name of the player),
    # You definitely want to change that.
    """
    global playerBoard, opponentBoard, targets, confirmShot, guessList, ges
    #if we just got a hit add the surrounding blocks as educated guesses to targets array
    if confirmShot['killed'] == const.HIT:
	for rack in opponentBoard:
		print rack
	#time.sleep(10)
	counter = 0
	print 'Confirmed kill at: (' + str(confirmShot['x']) + "," + str(confirmShot['y']) + ')'
	i = range(-1,2)
	for Xer in i:
		for Yer in i:
			x = confirmShot['x'] + Xer
			y = confirmShot['y'] + Yer	
			if XYValid(x,y) and not (Xer**2 == Yer**2):
			    counter = counter + 1
			    if noSecondGuess(x,y,opponentBoard,targets):
				 targets.append({'x': x, 'y' : y})
				

	
    #if we haven't got any educated guesses make a random one
    if len(targets)==0:
	    try:
    	        targets.append(guessList.pop())
		ges +=1
	    except:
		print 'board error'
    try:
	target = targets.pop()
    except IndexError:
	target = {'x' : 5, 'y' : 5}	
	print 'pop ERROR!'
    print 'Targets length:' + str(targets) + "Ges: " + str(ges)
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
    initBoards()
    initGuessList()

def newPlayer():
    """
    This method is used for backward compatibility. It will not be used during the competition. 
    You should ignore this function.
    """
    pass
