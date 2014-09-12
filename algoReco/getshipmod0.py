import math
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
validCombinations = [[],[],[],[],[]]
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
board = [[0]*12 for x in range(12)]
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
shotList = [{'x':8,'y':4}]

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
