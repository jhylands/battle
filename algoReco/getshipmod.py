from random import randint #import random numbers
import math
import time
#function to add two vectors
def addVector(A,B):
    return {'x':(A['x']+B['x']),'y':(A['y']+B['y'])}
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
def findMax(array):
    max = 0
    for i in range(0,len(array)):
	for n in range(0,len(array[i])):
	   if max < array[i][n]:
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
	    board[int(round(coordinates['x'])+x)][int(round(coordinates['y'])+y)] += 1
shotList = []
for loop in range(0,42):
    #look for posible positions of ships
    for shipNo in range(0,len(ships)):
        for rotation in range(0,shipSpin[shipNo]):
	    for x in range(0,12):
	        for y in range(0,7):
		    testShip(shipNo,x,y,rotation,shotList)
	        if x>6:
	            for y in range(7,12):
		        testShip(shipNo,x,y,rotation,shotList)
    shotList.append(findMax(board))
    board = [[0]*12 for x in range(12)]
print shotList
#look for posible conflics between 2 ships
dualshipValid = []
#compare ships
#for ship1No in range(0,5):
 #   for ship2No in range(ship1No,4):
#	#At this level we are looking at the conflicts between two ships
#	#compare placement solutions
#	counter = 0
#	for ship1Combination in range(0,len(validCombinations[ship1No])):
#	    for ship2Combination in range(ship1Combination,len(validCombinations[ship2No])):
#		#at this level we are looking at the conflics between two combinations of posible alinments of two ships
#		possibleCombo = True
#		#compare pannels
#		for ship1Pannel in range(0,len(ships[ship1No])):
#		    for ship2Pannel in range(ship1Pannel,len(ships[ship2No])):
#			#At this level we are looking at conflics between two pannels of two ships in a particular alignment of two ships
#			#(get ship part rotate it add coordinates) compare (get ship part rotate it add coordinates)
#			ship1 = addVector(doRotation(ships[ship1No][ship1Pannel],validCombinations[ship1No][ship1Combination]['rotation']),validCombinations[ship1No][ship1Combination])
#			ship2 = addVector(doRotation(ships[ship2No][ship2Pannel],validCombinations[ship2No][ship2Combination]['rotation']),validCombinations[ship2No][ship2Combination])
#			if ship1 == ship2:
#				counter = counter + 1
#				possibleCombo = False
#		if possibleCombo:
#		    dualshipValid.append({'ship1':ship1No,'ship2':ship2No,'ship1combonation':ship1Combination,'ship2Combination':ship2Combination})
#	print counter

f = open('validCombinations.dat','w')
f.write("single = " + str(validCombinations))
#f.write(str(dualshipValid))
f.close()
board = [['0']*12 for x in range(12)]
for shot in shotList:
    board[shot['x']][shot['y']] = "-"
for row in board:
    print row
