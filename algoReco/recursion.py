#import math for rotations
import math

#TRANSFORMATION FUNCTIONs----------------------------------------------------------------
#add vectors A and B
def addVector(A,B):
    return {'x':A['x']+B['x'],'y':A['y']+B['y']}
#takes B from A
def takeBFromA(A,B):
	return addVector(A,{'x':(-1 * B['x']),'y':(-1 * B['y'])})
#carry out a rotation in euclidian space
def rotate(coordinates,angle):
    #get the coordinates to local variables so its easyer to see whats going on
    x = coordinates['x']
    y = coordinates['y']
    X = round(x * math.cos(angle) - y * math.sin(angle))
    Y = round(x * math.sin(angle) + y * math.cos(angle))
    return {'x':X,'y':Y}
#converting from battleship coordinate system to normal one with origin 11,0 in battle ship coordinates
def ZtoW(coordinates):
    u = coordinates['y']
    v = -coordinates['x']
    return {'x': u ,'y': v }
#a function such that WtoZ(ZtoW(coordinates)) = coordinates
def WtoZ(coordinates):
    u = -coordinates['y']
    v = coordinates['x']
    return {'x':u,'y':v}
#carry out a rotation in battleship space
def doRotation(coordinates,angle):
    return WtoZ(rotate(ZtoW(coordinates),angle))
#-----------------------------------------------------------------------------------------------

#DEFINE THE SHIPS----------------------------------------------------------------------------------
#array of all the ships
ships =[]
#array of the spin of each ship
shipSpin = [2,2,2,4,4]
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
#-----------------------------------------------------------------------------------------------------
#MAIN ALGORITHM---------------------------------------------------------------------------------------


#function to inishiate a board and add the misses to it
#fin
def createBoard(missList):
#    try:
#	board = [[False]*(6 if x<6 else 12) for x in range(12)]
#	for miss in missList:
##	    board[miss['x']][miss['y']] = True
#    except:
#	print missList
    board = [[False]*(6 if x<6 else 12) for x in range(12)]
    return board

#function to add ship to board
#fin
def addToBoard(board,shipCoords):
    try:
	for coord in shipCoords:
            if not board[coord['x']][coord['y']]:
	        board[coord['x']][coord['y']] = True
	    else:
	        return False, Board
	        break
        else:
	    return True,board
    except:
	return False, board

#function to check that none of the blob is uncovered by the combination
#fin
def blobCovered(board,hitList):
    for hit in hitList:
	if not board[hit['x']][hit['y']]:
	    return False
	    break
    else:
	return True

#add combination to validCombinations
#function to get an array of the ships coordinates given its rotation and origin
#fin
def getShipCoords(aShip,position,rotation,origin):
    global ships, shipSpin
    coords = []
    for pannel in ships[aShip]:
	coords.append(doRotation(pannel,shipSpin[aShip]*math.pi/2))
    originTransformer = coords[origin]
    for x in range(0,len(coords)):
	coords[x] = addVector(position,takeBFromA(coords[x],originTransformer))
    return coords


#function to list valid combinations give a list of ships, their position rotation and origin
def checkCombinations(shipList,placementList,rotationList,pannelList,hitList,missList):
    validCombinations = []
    #create the board with the misses already on
    oriBoard = createBoard(missList)
    #select a set of rotations
    for rotation in rotationList:
	#select a set of pannels as origins
	for origin in pannelList:
	    #select a set of positions to place those origins
	    for placement in placementList:
		#resetboard
	    	board = list(oriBoard)
	    	shipCoords = []
	    	for x in range(0,len(shipList)):
		    shipCoords += getShipCoords(shipList[x],hitList[placement[x]],rotation[x],origin[x])
		    valid,board = addToBoard(board,shipCoords)
	    	if valid and blobCovered(board,hitList):
		    validCombination += shipCoords
    return validCombinations

#fucntion to loop through each pannel of each ship
#arr[combination][ship] = ships origin
#fin
def addPannels(shipList,mainList = [],countingList = []):
    global ships
    #pop ship from array for use on this recusion level
    ship = shipList.pop()
    #get the number of rotations for this ship
    pannels = len(ships[ship])
    #loop through each rotation
    for x in range(0,pannels):
	#add this rotation to the counting list
        countingList.append(x)
	#if we don't need to go any deeper add the counting array as an element of the main list
	if len(shipList) ==0:
	    mainList.append(list(countingList))
	else:
	    #otherwise recure deeper updating mainlist
	    mainList = addPannels(shipList,mainList,countingList)
	#remove this loops countingList contribution so next loop can take its place
	countingList.pop()
    #return the mainlist
    shipList.append(ship)
    return mainList

#fucntion to create an array of posible rotation configerations for the ships
#arr[arrangment][ship]
#fin
def addRotary(ships,mainList = [],countingList = []):
    global shipSpin
    #pop ship from array for use on this recusion level
    ship = ships.pop()
    #get the number of rotations for this ship
    rotations = shipSpin[ship]
    #loop through each rotation
    for x in range(0,rotations):
	#add this rotation to the counting list
        countingList.append(x)
	#if we don't need to go any deeper add the counting array as an element of the main list
	if len(ships) == 0:
	    mainList.append(list(countingList))
	else:
	    #otherwise recure deeper updating mainlist
	    mainList = addRotary(ships,mainList,countingList)
	#remove this loops countingList contribution so next loop can take its place
	countingList.pop()
    #return the mainlist
    ships.append(ship)
    return list(mainList)


#function to place the ships in their plain of the hitlist
def addPlacement(ships,hitListLength,start = None, mainList = None,countingList = None):
    if start == None:
	start=0
    if mainList == None:
	mainList = []
    if countingList == None:
	countingList = []
    #pop ship from array for use on this recusion level
    ship = ships.pop()
    #loop through each hit
    for x in range(start,hitListLength):
	#add this rotation to the counting list
        countingList.append(x)
	#if we don't need to go any deeper add the counting array as an element of the main list
	if len(ships) == 0:
	    mainList.append(list(countingList))
	else:
	    #otherwise recure deeper updating mainlist
	    mainList += addPlacement(ships,hitListLength,(start+1),mainList,countingList)
	#remove this loops countingList contribution so next loop can take its place
	countingList.pop()
    #return the mainlist
    ships.append(ship)
    return list(mainList)

#function to gather the information required to find the next best shot
def test(shipList,hitList,missList):
	#assign all the ships possitions
	placementList= addPlacement(shipList,len(hitList))
	#get them each a rotation
	rotationList = addRotary(shipList,[])
	#get them each an origin
	originList = addPannels(shipList,[])
	#placementList[placementCombination][ship]
	#rotationlist[rotationCombination][ship]
	#originList[pannelCombination][ship]
	return checkCombinations(shipList,placementList,rotationList,originList,hitList,missList)

#shipList is a list of the ships to use in current test
#hitList is a list of hits in blob that must be covered
#NotList is a list of ships not to be used in futher loops
#main function - top of recusion list
#test() calls need to be replaced with a function that will take a 
#list of ships and output a list of possible valid combinations
def recursion(hitList,shipList = None, missList = None, notList = None, n = None):
    #if not shipList provided set it as empty array
    if shipList == None:
	shipList = []
    #if no misses have been reported (lucky first shot) then inishiate missList as empty array
    if missList == None:
	missList = []
    #if no notlist provided as parameter then set is as empty array
    if notList == None:
	notList = []
    #if n not provided take 5 a defualt
    if n == None:
	n=5
    #inisiate list of valid combinations
    validList=[]
    #loop through ships
    for i in range(0,n):
	#but not ships already in use as each ship can only appear once
	if not i in notList:
	    #check for possibles using the ship proposed by current value of i in the loop and the other ships added in higher branches of the recursion
	    shipList.append(i)#add current ship to shipList
     	    validList += test(shipList,hitList,missList)
	    #if there are more hits then we have ships, look at possibilities that use more ships
	    if len(hitList)>len(notList) and len(notList)<5:
		#for futher recurtions remove i (the current ship represented by I) from the loops
	        notList.append(i)
		#use more ships in check
 		validList += recursion(hitList,missList, shipList,notList,n)
		#remove this ship from notlist as i is about to change to a new value
	        notList.pop()
	    #remove i from shipList as i is about to change
	    shipList.pop()
    return validList

		
#OUTSIDE OF FINDING VALID COMBINATONS ----------------------------------------------------------
#finds the best coordinates on the board
def findMax(array):
    max = 0
    for i in range(0,len(array)):
	for n in range(0,len(array[i])):
	   if max <= array[i][n]:
		max = array[i][n]
		coordinates = {'x':i,'y':n}
    return coordinates


