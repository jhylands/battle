
def initGuessList():
    for i in range(0,11,2):
	for n in range(0,11,2):
	    if XYValid(n,i):
		guessList.append({'x' : n, 'y' : i})
    for i in range(1,11,2):
	for n in range(1,11,2):
	    if XYValid(n,i):
		guessList.append({'x' : n, 'y' : i})
def XYValid(x,y):
    if ((x>=0) and (y>=0) and (x<12 and y<12)) and ((x>5 and y>5) or (y<6)):
	return True
    else:
	return False

guessList = []
initGuessList() 
print guessList
