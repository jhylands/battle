from random import randint
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
def XYValid(x,y):
    if ((x>=0) and (y>=0) and (x<12 and y<12)) and ((x>5 and y>5) or (y<6)):
	return True
    else:
	return False
board = [[0]*12 for x in range(12)]
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
for rach in board:
	print rach
