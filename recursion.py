#import math for rotations
import math

#TRANSFORMATION FUNCTIONs----------------------------------------------------------------
#add vectors A and B
def addVector(A,B)
    return {'x':A['x']+B['x'],'y':A['y']+B['y']}
#takes B from A
def takeBFromA(A,B):
	return addVector(A,{'x':(-1 * B['x']),'y':(-1 * B['y'])})
#carry out a rotation in euclidian space
def rotate(coordinates,angle):
    #get the coordinates to local variables so its easyer to see whats going on
    x = coordinates['x']
    y = coordinates['y']
    X = x * math.cos(angle) - y * math.sin(angle)
    Y = x * math.sin(angle) + y * math.cos(angle)
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
#check the validity of coordinates
def XYValid(x,y,notHere = None):
    if notHere is None:
	notHere = []
    if ((x>=0) and (y>=0) and (x<12 and y<12)) and ((x>5 and y>5) or (y<6)):
	Valid = True
	for notPoint in notHere:
	    if x==notPoint['x'] and y==notPoint['y']:
		Valid = False
	return Valid
    else:
	return False

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

#shipList is a list of the ships to use in current test
#hitList is a list of hits in blob that must be covered
#NotList is a list of ships not to be used in futher loops
#main function - top of recusion list
#test() calls need to be replaced with a function that will take a 
#list of ships and output a list of possible valid combinations
def recursion(hitList,shipList = None, missList = None, Notlist = None, n = None):
    #if not shipList provided set it as empty array
    if shipList == None:
	shipList = []
    #if no misses have been reported (lucky first shot) then inishiate missList as empty array
    if missList == None:
	missList = []
    #if no notlist provided as parameter then set is as empty array
    if Notlist == None:
	Notlist = []
    #if n not provided take 5 a defualt
    if n == None:
	n=5

    #inisiate list of valid combinations
    validList=[]

    #loop through ships
    for i in range(0,n):
	#but not ships already in use as each ship can only appear once
	if not i in NotList:
	    #check for possibles using the ship proposed by current value of i in the loop and the other ships added in higher branches of the recursion
	    shipList.append(i)#add current ship to shipList
     	    validList += blobSelection(shipList,hitList,MissList)
	    #if there are more hits then we have ships, look at possibilities that use more ships
	    if len(hitList)>len(NotList):
		#for futher recurtions remove i (the current ship represented by I) from the loops
	        NotList.append(i)
		#use more ships in check
 		ValidList += recursion(hitList,missList, shipList,Notlist,n)
		#remove this ship from notlist as i is about to change to a new value
	        Notlist.pop()
	    #remove i from shipList as i is about to change
	    shipList.pop()
    return validList

#fucntion to create an array of posible rotation configerations for the ships
#arr[arrangment][ship]
#fin
def addRotaty(ships,mainList = [],CountingList = []):
    #pop ship from array for use on this recusion level
    ship = ships.pop()
    #get the number of rotations for this ship
    rotations = shipRotations[ship['ship']]
    #loop through each rotation
    for x in range(0,rotations):
	#add this rotation to the counting list
        countingList.append(x)
	#if we don't need to go any deeper add the counting array as an element of the main list
	if len(ships) ==0:
	    mainList.append(countingList)
	else:
	    #otherwise recure deeper updating mainlist
	    mainList = addRotary(mainList,countinglist)
	#remove this loops countingList contribution so next loop can take its place
	countingList.pop()
    #return the mainlist
    return mainList


#place the ships on the blobs
#fin
def BlobSelection(shipList,hitList,missList,shipPlace = None):
    #define an empty valid list
    validList = []
    #if there are no ships yet possitioned
    if shipPlace == None:
	shipPlace = []
    #if there are no ships left to position check if the current formation a ships has many valid combinations (of rotation and mixed origin)
    if len(shipPlace) == len(shipList):
	#all ships assigned a place
	#get them each a rotation
	rotationList = addRotary(shipPlace)
	#get them each an origin
	OriginList = addPannels(shipPlace)
	#shipPlace{'ship','x','y'}
	#rotationlist[rotationCombination][ship]
	#originList[pannelCombination][ship]
	#apply transformations and check if valid
	validList += checkCombinations(shipPlace,rotationList,OriginList,hitList,missList)
    else:
	for place in hitList:
	    shipPlace.append({'ship':shipList.pop(),'x':place['x'],'y' : place['y']})
	    #add the recursive valid options to the valid list
	    validList += BlobSelection(shipList, hitList, missList, shipPlace)
    return validList
#fucntion to loop through each pannel of each ship
#arr[combination][ship] = ships origin
#fin
def addPannels(ships,mainList = [],CountingList = []):
    #pop ship from array for use on this recusion level
    ship = ships.pop()
    #get the number of rotations for this ship
    pannels = len(Globalships[ship['ship']])
    #loop through each rotation
    for x in range(0,pannels):
	#add this rotation to the counting list
        countingList.append(x)
	#if we don't need to go any deeper add the counting array as an element of the main list
	if len(ships) ==0:
	    mainList.append(countingList)
	else:
	    #otherwise recure deeper updating mainlist
	    mainList = addPannels(mainList,countinglist)
	#remove this loops countingList contribution so next loop can take its place
	countingList.pop()
    #return the mainlist
    return mainList

#function to inishiate a board and add the misses to it
#fin
def createBoard(missList):
    board = [[False]*(6 if x<6 else 12) for x in range(12)]
    for miss in missList:
	board[miss['x']][miss['y']] = True
    return board

#function to add ship to board
#fin
def addToBoard(board,shipCoords):
    for coord in shipCoords:
	if not board[coord['x']][coord['y']]:
	    board[coord['x']][coord['y']] = True
	else:
	    return False, Board
	    break
    else:
	return True,board
#function to check that none of the blob is uncovered by the combination
#fin
def blobCovered(board,hitList):
    for hit in hitList:
	if not board[hit['x']][hit['y']]
	    return False
	    break
    else:
	return True

#function to list valid combinations give a list of ships, their position rotation and origin
def checkCombinations(shipPlace,rotationList,pannelList,hitList,missList):
    validCombinations = []
    #create the board with the misses already on
    oriBoard = createBoard(missList)
    for rotation in rotationList:
	for origin in pannelList:
	    #for a rotation list and an origin list 
	    board = oriBoard
	    shipCoords = []
	    for x in range(0,len(shipPlace)):
		shipCoords += getShipCoords(shipPlace[x],rotation[x],origin[x])
	    valid,board = addToBoard(board,shipCoords)
	    if valid and blobCovered(board,hitList):
			validCombination += shipCoords
    return validCombinations
		
		#add combination to validCombinations
#function to get an array of the ships coordinates given its rotation and origin
#fin
def getShipCoords(aShip,rotation,origin):
    global ships, shipSpin
    coords = []
    for pannel in ships[shipPlace['ship']]:
	coords.append(doRotation(pannel,shipSpin[ships[shipPlace['ship']]]))
    originTransformer = coords[origin]
    for x in range(0,len(coords)):
	coords[x] = addVector(aShip,takeBFromA(coords[x],originTransformer))
    return coords









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
#array to hold possible combinations

#function that tests if a ship is possible given the ship, its position, rotation and any misses on the board
def testShip(shipNo,x,y,rotaryMultiple,invalid = None):
    if invalid is None:
	invalid = []
    angle = math.pi*rotaryMultiple/2
    valid = True
    for pannel in ships[shipNo]:
	coordinates = doRotation(pannel,angle)
        if not XYValid(round(coordinates['x'])+x,round(coordinates['y'])+y,invalid):
	    valid = False
    if valid:
	validCombinations[shipNo].append({'rotation':rotaryMultiple,'x':x,'y':y})
	for pannel in ships[shipNo]:
	    coordinates = doRotation(pannel,angle)
	    board[int(round(coordinates['x']+x))][int(round(coordinates['y']+y))] +=1

#look for posible positions of ships
#for each ship
for shipNo in range(0,len(ships)):
    #for each rotation of that ship
    for rotation in range(0,shipSpin[shipNo]):
	#for each x 
	for x in range(0,12):
     	    for y in range(0,7):
  		testShip(shipNo,x,y,rotation,shotList)
            if x>6:
         	for y in range(7,12):
      		    testShip(shipNo,x,y,rotation,shotList)
		
shotList.append(findMax(board))
for row in board:
    print row
print shotList

