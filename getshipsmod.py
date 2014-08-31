from random import randint #import random numbers
import math
import time
def rotate(coordinates,angle):
    #get the coordinates to local variables so its easyer to see whats going on
    x = coordinates['x']
    y = coordinates['y']
    xN = y
    yN = -x
    X = int(xN * math.cos(angle) - yN * math.sin(angle))
    Y = int(xN * math.sin(angle) + yN * math.cos(angle))
    Xn = - Y
    Yn = X
    return {'x':Xn,'y':Yn}
#array to hold possible combinations
validCombinations = []
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
def XYValid(x,y):
    if ((x>=0) and (y>=0) and (x<12 and y<12)) and ((x>5 and y>5) or (y<6)):
	return True
    else:
	return False
board = [[0]*12 for x in range(12)]

def testShip(shipNo,x,y,rotation):
    angle = math.pi*rotation/2
    valid = True
    for pannel in ships[shipNo]:
	coordinates = rotate(pannel,angle)
        if not XYValid(coordinates['x']+x,coordinates['y']+y):
	    valid = False
    if valid:
	validCombinations.append({'ship':shipNo,'rotation':rotation,'x':x,'y':y})

def getBoard():
	for ship in ships:
	    #chose random position
	    invalidPosition = True
	    while invalidPosition:
		col = randint(0,11)
		row = randint(0,11)
		thisTrans=True
		#look to see if the position is valid
		for element in ship:
		    if not (XYValid(element['x']+col,element['y']+row) and board[element['x']][element['y']]==0):
			thisTrans = False	
		if thisTrans:
		    invalidPosition = False
		    for element in ship:
			element['x'] = element['x']+col
			element['y'] = element['y']+row
			board[element['x']][element['y']] = 8

for shipNo in range(0,len(ships)):
    for rotation in range(0,shipSpin[shipNo]):
	for x in range(0,12):
	    for y in range(0,7):
		testShip(shipNo,x,y,rotation)
	    if x>6:
		for y in range(7,12):
		    testShip(shipNo,x,y,rotation)

f = open('validCombinations.dat','w')
f.write(str(validCombinations))
f.close()
print rotate({'x': 1, 'y': 0},math.pi/2)
