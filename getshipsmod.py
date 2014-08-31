from random import randint #import random numbers
import math
import time
def rotate(coordinates,angle):
    #get the coordinates to local variables so its easyer to see whats going on
    x = coordinates['x']
    y = coordinates['y']
    X = int(x * math.cos(angle) - y * math.sin(angle))
    Y = int(x * math.sin(angle) + y * math.cos(angle))
    return {'x':X,'y':Y}
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
print rotate({'x': -3, 'y': -1},math.pi*3/2)
print rotate({'x': -3, 'y': 0},math.pi*3/2)
print rotate({'x': -3, 'y': 1},math.pi*3/2)
print rotate({'x': 0, 'y': 0},math.pi*3/2)
print rotate({'x': -1, 'y': 0},math.pi*3/2)
print rotate({'x': -2, 'y': 0},math.pi*3/2)
print 'GAP'
for pannel in ships[3]:
    coordinates = rotate(pannel,(math.pi*3/2))
    print coordinates
    if not XYValid(coordinates['x']+11,coordinates['y']+11):
        print "No big motherfucking error!"
